"""
Request models for the Lunar Solar Simulator API.
"""
from typing import Literal
from pydantic import BaseModel, Field, field_validator


class SimulationRequest(BaseModel):
    """
    Input parameters for running a lunar solar energy simulation.
    
    Attributes:
        ring_width_km: Width of the solar panel ring on the Moon's equator (1-500 km)
        panel_efficiency: Solar panel conversion efficiency (0.1-0.5 or 10%-50%)
        transmission_type: Energy transmission method - 'microwave' or 'laser'
        num_ground_stations: Number of Earth receiving stations (1-50)
        simulation_hours: Duration of simulation in hours (1-168, max 1 week)
    """
    ring_width_km: float = Field(
        ..., 
        gt=0, 
        le=500,
        description="Width of the solar panel ring in kilometers"
    )
    panel_efficiency: float = Field(
        ..., 
        gt=0, 
        le=1,
        description="Solar panel efficiency (0.0 to 1.0)"
    )
    transmission_type: Literal["microwave", "laser"] = Field(
        ...,
        description="Energy transmission method"
    )
    num_ground_stations: int = Field(
        ..., 
        gt=0, 
        le=50,
        description="Number of ground receiving stations"
    )
    simulation_hours: int = Field(
        ..., 
        gt=0, 
        le=168,
        description="Simulation duration in hours (max 1 week)"
    )
    
    # Optional advanced parameters for Phase 2
    include_lunar_cycle: bool = Field(
        default=False,
        description="Include lunar day/night cycle effects"
    )
    include_atmospheric_effects: bool = Field(
        default=False,
        description="Include Earth atmospheric absorption"
    )
    lunar_day_hour: float = Field(
        default=354.0,
        ge=0,
        le=708,
        description="Current hour in lunar day cycle (0-708 hours)"
    )

    @field_validator('panel_efficiency')
    @classmethod
    def validate_efficiency(cls, v: float) -> float:
        if v < 0.05:
            raise ValueError('Panel efficiency below 5% is unrealistic')
        if v > 0.50:
            raise ValueError('Panel efficiency above 50% exceeds current technology')
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ring_width_km": 50,
                    "panel_efficiency": 0.22,
                    "transmission_type": "microwave",
                    "num_ground_stations": 5,
                    "simulation_hours": 24
                }
            ]
        }
    }