from fastapi import FastAPI, HTTPException
from models.input_model import SimulationInput
from simulation.orchestrator import Simulation
import plotly.graph_objects as go
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Lunar Solar Simulation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sim = Simulation()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/simulate")
def run_simulation(input_data: SimulationInput):
    try:
        result = sim.run(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/simulate-with-graph")
def run_simulation_with_graph(input_data: SimulationInput):
    result = sim.run(input_data)

    graph = generate_graph(
        result["total_energy_generated_gw"],
        result["energy_received_gw"]
    )

    return {
        "result": result,
        "graph": graph
    }

def generate_graph(generated, received):
    fig = go.Figure()

    fig.add_bar(name="Generated", x=["Energy"], y=[generated])
    fig.add_bar(name="Received", x=["Energy"], y=[received])

    fig.update_layout(title="Energy Comparison")

    return fig.to_json()
