from pydantic import BaseModel, Field

class SimulationInput(BaseModel):
    ring_width_km: float = Field(gt=0, lt=500)
    panel_efficiency: float = Field(gt=0, lt=1)
    transmission_type: str
    num_ground_stations: int = Field(gt=0, lt=100)

    class Config:
        schema_extra = {
            "example": {
                "ring_width_km": 50,
                "panel_efficiency": 0.22,
                "transmission_type": "microwave",
                "num_ground_stations": 5
            }
        }