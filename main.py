# main.py

from simulation.orchestrator import Simulation
from models.input_model import SimulationInput

sim = Simulation()

input_data = SimulationInput(
    ring_width_km=100,
    panel_efficiency=0.22,
    transmission_type="microwave",
    num_ground_stations=5
)

result = sim.run(input_data)
print(result)