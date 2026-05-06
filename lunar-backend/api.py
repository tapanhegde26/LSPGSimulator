"""
Lunar Solar Simulator API
FastAPI application providing REST and WebSocket endpoints for simulation.
"""
import asyncio
import random
from typing import Literal, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, HTMLResponse
from pydantic import BaseModel

from config import settings
from models.request import SimulationRequest
from models.response import SimulationResponse, HealthResponse, OptimizationResult
from services.simulation_service import run_simulation
from services.energy_model import calculate_energy
from services.transmission_model import calculate_transmission
from services.parameter_optimizer import optimize_parameters, quick_optimize, OptimizationConstraints
from services.export_service import export_to_json, export_to_csv, generate_report_html
from utils.logger import logger


# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A simulation platform for modeling space-based solar power transmission from the Moon to Earth",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


# Request models for new endpoints
class OptimizationRequest(BaseModel):
    target_energy_gw: Optional[float] = None
    budget_constraint: Optional[float] = None
    optimization_goal: Literal["maximize_energy", "maximize_efficiency", "minimize_cost"] = "maximize_energy"
    n_trials: int = 50


class QuickOptimizeRequest(BaseModel):
    ring_width_km: float
    panel_efficiency: float
    transmission_type: str
    num_ground_stations: int


@app.get("/", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    Returns the current status of the API and its version.
    """
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        simulation_ready=True
    )


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health() -> HealthResponse:
    """Alias for health check endpoint."""
    return await health_check()


@app.post("/simulate", response_model=SimulationResponse, tags=["Simulation"])
def simulate(request: SimulationRequest) -> SimulationResponse:
    """
    Run a complete lunar solar energy simulation.
    
    This endpoint performs the full simulation pipeline:
    1. Calculate energy generation from the lunar ring
    2. Apply transmission losses (microwave or laser)
    3. Distribute energy across ground stations
    4. Generate time series data
    5. Produce AI-powered insights
    
    Returns comprehensive simulation results including energy metrics,
    station distribution, time series data, and recommendations.
    """
    try:
        logger.info(f"Simulation request: ring={request.ring_width_km}km, "
                   f"efficiency={request.panel_efficiency}, "
                   f"transmission={request.transmission_type}")
        return run_simulation(request)
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Simulation error: {e}")
        raise HTTPException(status_code=500, detail="Simulation failed")


@app.post("/optimize", tags=["Optimization"])
def optimize(request: OptimizationRequest):
    """
    Find optimal simulation parameters using AI optimization.
    
    Uses Optuna to search for the best combination of:
    - Ring width
    - Panel efficiency
    - Number of ground stations
    - Transmission type
    
    Optimization goals:
    - maximize_energy: Find parameters that produce most energy
    - maximize_efficiency: Find most efficient configuration
    - minimize_cost: Find cheapest configuration meeting target
    """
    try:
        logger.info(f"Optimization request: goal={request.optimization_goal}")
        
        constraints = OptimizationConstraints(
            budget_constraint=request.budget_constraint
        )
        
        result = optimize_parameters(
            target_energy_gw=request.target_energy_gw,
            constraints=constraints,
            n_trials=request.n_trials,
            optimization_goal=request.optimization_goal,
        )
        
        return result
    except Exception as e:
        logger.error(f"Optimization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/optimize/quick", tags=["Optimization"])
def quick_optimize_endpoint(request: QuickOptimizeRequest):
    """
    Get quick optimization suggestions based on current parameters.
    
    Analyzes the current configuration and suggests improvements
    without running full optimization.
    """
    try:
        result = quick_optimize({
            "ring_width_km": request.ring_width_km,
            "panel_efficiency": request.panel_efficiency,
            "transmission_type": request.transmission_type,
            "num_ground_stations": request.num_ground_stations,
        })
        return result
    except Exception as e:
        logger.error(f"Quick optimize error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/export/json", tags=["Export"])
def export_json(request: SimulationRequest, include_time_series: bool = True):
    """
    Run simulation and export results as JSON.
    """
    try:
        result = run_simulation(request)
        json_data = export_to_json(result, include_time_series=include_time_series)
        return Response(
            content=json_data,
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=simulation_results.json"}
        )
    except Exception as e:
        logger.error(f"Export error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/export/csv", tags=["Export"])
def export_csv(
    request: SimulationRequest,
    data_type: Literal["summary", "time_series", "stations"] = "time_series"
):
    """
    Run simulation and export results as CSV.
    
    Data types:
    - summary: Key metrics
    - time_series: Hourly energy data
    - stations: Ground station distribution
    """
    try:
        result = run_simulation(request)
        csv_data = export_to_csv(result, data_type=data_type)
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=simulation_{data_type}.csv"}
        )
    except Exception as e:
        logger.error(f"Export error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/export/report", response_class=HTMLResponse, tags=["Export"])
def export_report(request: SimulationRequest):
    """
    Run simulation and generate an HTML report.
    
    Returns a standalone HTML page with charts and analysis.
    """
    try:
        result = run_simulation(request)
        html = generate_report_html(result)
        return HTMLResponse(content=html)
    except Exception as e:
        logger.error(f"Report generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/simulate")
async def simulate_ws(websocket: WebSocket) -> None:
    """
    WebSocket endpoint for real-time simulation streaming.
    
    Accepts simulation parameters and streams time series data
    point by point, enabling real-time visualization.
    """
    await websocket.accept()
    logger.info("WebSocket connection established")

    try:
        data = await websocket.receive_json()
        logger.info(f"WebSocket simulation request received")

        # Validate transmission type
        transmission_type: Literal["microwave", "laser"] = data.get("transmission_type", "microwave")
        if transmission_type not in ("microwave", "laser"):
            transmission_type = "microwave"

        base_energy = calculate_energy(
            data["ring_width_km"],
            data["panel_efficiency"],
        )

        simulation_hours = min(data.get("simulation_hours", 24), settings.max_simulation_hours)

        for hour in range(simulation_hours):
            variation = random.uniform(0.95, 1.05)
            generated = base_energy * variation
            received, loss = calculate_transmission(generated, transmission_type)

            await websocket.send_json({
                "time_hour": hour,
                "energy_generated_gw": round(generated, 2),
                "energy_received_gw": round(received, 2),
                "transmission_loss_percent": round(loss, 2),
            })

            await asyncio.sleep(0.15)  # Stream delay for visualization

        # Send completion signal
        await websocket.send_json({"status": "complete", "total_hours": simulation_hours})
        logger.info("WebSocket simulation completed")

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except KeyError as e:
        logger.error(f"Missing required field: {e}")
        await websocket.send_json({"error": f"Missing required field: {e}"})
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.send_json({"error": str(e)})
    finally:
        try:
            await websocket.close()
        except Exception:
            pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )