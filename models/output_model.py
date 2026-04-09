# models/output_model.py

from pydantic import BaseModel

class SimulationOutput(BaseModel):
    total_energy_generated_gw: float
    energy_received_gw: float
    transmission_loss_percent: float
    system_efficiency: float