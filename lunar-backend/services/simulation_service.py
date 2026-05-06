"""
Simulation orchestration service.
Coordinates the entire simulation pipeline from energy generation to insights.
"""
import random
from typing import List, Dict, Any

from models.request import SimulationRequest
from models.response import SimulationResponse, GroundStationOutput, TimeSeriesPoint
from services.energy_model import calculate_energy
from services.transmission_model import calculate_transmission
from services.earth_model import distribute_energy
from services.optimization_service import generate_insights
from utils.logger import logger


def run_simulation(request: SimulationRequest) -> SimulationResponse:
    """
    Execute the complete simulation pipeline.
    
    Args:
        request: Validated simulation input parameters
        
    Returns:
        SimulationResponse with all computed results and insights
        
    Raises:
        Exception: If any step in the simulation fails
    """
    try:
        logger.info("Starting simulation")

        # Step 1: Energy Generation
        total_energy = calculate_energy(
            request.ring_width_km,
            request.panel_efficiency,
        )
        logger.info(f"Energy generated: {total_energy:.2f} GW")

        # Step 2: Transmission
        received_energy, loss_percent = calculate_transmission(
            total_energy,
            request.transmission_type,
        )
        logger.info(f"Energy received: {received_energy:.2f} GW (loss: {loss_percent:.1f}%)")

        # Step 3: Distribution
        stations_data = distribute_energy(
            received_energy,
            request.num_ground_stations,
        )
        stations = [
            GroundStationOutput(**station)
            for station in stations_data
        ]

        # Step 4: Time Series Generation
        time_series = generate_time_series(request, total_energy)

        # Step 5: Calculate Efficiency
        efficiency = received_energy / total_energy if total_energy > 0 else 0.0

        # Step 6: Generate Insights
        insights = generate_insights(
            request,
            {
                "system_efficiency": efficiency,
                "total_energy": total_energy,
                "received_energy": received_energy,
            }
        )

        logger.info("Simulation completed successfully")

        return SimulationResponse(
            total_energy_generated_gw=total_energy,
            energy_received_gw=received_energy,
            transmission_loss_percent=loss_percent,
            system_efficiency=efficiency,
            stations=stations,
            time_series=time_series,
            insights=insights
        )

    except Exception as e:
        logger.error(f"Simulation failed: {str(e)}")
        raise


def generate_time_series(
    request: SimulationRequest, 
    base_energy: float
) -> List[TimeSeriesPoint]:
    """
    Generate time series data simulating energy variation over time.
    
    Args:
        request: Simulation parameters including duration
        base_energy: Base energy generation in GW
        
    Returns:
        List of TimeSeriesPoint objects for each hour
    """
    time_series: List[TimeSeriesPoint] = []

    for hour in range(request.simulation_hours):
        # Simulate fluctuation (±5%)
        variation = random.uniform(0.95, 1.05)
        generated = base_energy * variation

        received, _ = calculate_transmission(
            generated,
            request.transmission_type,
        )

        time_series.append(
            TimeSeriesPoint(
                time_hour=hour,
                energy_generated_gw=generated,
                energy_received_gw=received,
            )
        )

    return time_series