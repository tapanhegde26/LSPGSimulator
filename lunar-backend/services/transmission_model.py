"""
Transmission Model for Lunar Solar Simulator
Calculates energy losses during Moon-to-Earth transmission.
"""
from typing import Tuple, Literal, Optional
from utils.constants import (
    MICROWAVE_BASE_LOSS,
    LASER_BASE_LOSS,
    ATMOSPHERIC_LOSS,
    EARTH_MOON_DISTANCE_KM,
)


def calculate_transmission(
    energy_gw: float, 
    transmission_type: Literal["microwave", "laser"],
    include_atmospheric_effects: bool = False,
    zenith_angle_deg: float = 30.0,
    weather_factor: float = 1.0,
    distance_km: Optional[float] = None,
) -> Tuple[float, float]:
    """
    Calculate energy received after transmission from Moon to Earth.
    
    Transmission losses include:
    - Base transmission losses (beam spreading, conversion)
    - Atmospheric absorption (if enabled)
    - Weather effects (if enabled)
    - Distance-based losses (if variable distance provided)
    
    Args:
        energy_gw: Energy to transmit in gigawatts
        transmission_type: 'microwave' or 'laser'
        include_atmospheric_effects: Enable detailed atmospheric modeling
        zenith_angle_deg: Angle from vertical for ground station (0-90)
        weather_factor: Weather condition (1.0=clear, 0.2=heavy rain)
        distance_km: Earth-Moon distance (uses mean if not provided)
        
    Returns:
        Tuple of (received_energy_gw, loss_percentage)
        
    Raises:
        ValueError: If transmission_type is not 'microwave' or 'laser'
    """
    if transmission_type == "microwave":
        base_loss = MICROWAVE_BASE_LOSS
    elif transmission_type == "laser":
        base_loss = LASER_BASE_LOSS
    else:
        raise ValueError(f"Invalid transmission type: {transmission_type}")

    total_loss = base_loss
    
    # Add atmospheric loss
    if include_atmospheric_effects:
        from services.physics_model import calculate_atmospheric_absorption
        atm_factor, atm_loss = calculate_atmospheric_absorption(
            zenith_angle_deg,
            weather_factor,
            transmission_type
        )
        total_loss += (1 - atm_factor)
    else:
        total_loss += ATMOSPHERIC_LOSS
    
    # Add distance-based beam spreading loss
    if distance_km is not None:
        from services.physics_model import calculate_beam_spreading_loss
        beam_factor = calculate_beam_spreading_loss(
            distance_km,
            transmission_type
        )
        # Beam spreading is multiplicative, not additive
        total_loss = 1 - (1 - total_loss) * beam_factor
    
    # Ensure loss doesn't exceed 100%
    total_loss = min(total_loss, 0.99)
    
    received_energy = energy_gw * (1 - total_loss)
    loss_percent = total_loss * 100

    return received_energy, loss_percent


def calculate_transmission_with_physics(
    energy_gw: float,
    transmission_type: Literal["microwave", "laser"],
    zenith_angle_deg: float = 30.0,
    weather_factor: float = 1.0,
    orbital_hour: float = 0.0,
) -> dict:
    """
    Calculate transmission with detailed physics breakdown.
    
    Args:
        energy_gw: Energy to transmit in gigawatts
        transmission_type: 'microwave' or 'laser'
        zenith_angle_deg: Ground station zenith angle
        weather_factor: Weather condition factor
        orbital_hour: Current hour in lunar orbit (for distance)
        
    Returns:
        Dictionary with detailed transmission breakdown
    """
    from services.physics_model import (
        calculate_earth_moon_distance,
        calculate_beam_spreading_loss,
        calculate_atmospheric_absorption,
    )
    
    # Calculate current Earth-Moon distance
    distance_km = calculate_earth_moon_distance(orbital_hour)
    
    # Base transmission loss
    if transmission_type == "microwave":
        base_loss = MICROWAVE_BASE_LOSS
    else:
        base_loss = LASER_BASE_LOSS
    
    # Beam spreading loss
    beam_factor = calculate_beam_spreading_loss(distance_km, transmission_type)
    beam_loss = 1 - beam_factor
    
    # Atmospheric absorption
    atm_factor, atm_loss_pct = calculate_atmospheric_absorption(
        zenith_angle_deg,
        weather_factor,
        transmission_type
    )
    atm_loss = 1 - atm_factor
    
    # Total loss (multiplicative)
    transmission_factor = (1 - base_loss) * beam_factor * atm_factor
    total_loss = 1 - transmission_factor
    
    received_energy = energy_gw * transmission_factor
    
    return {
        "received_energy_gw": received_energy,
        "total_loss_percent": total_loss * 100,
        "transmission_factor": transmission_factor,
        "breakdown": {
            "base_loss_percent": base_loss * 100,
            "beam_spreading_loss_percent": beam_loss * 100,
            "atmospheric_loss_percent": atm_loss * 100,
            "distance_km": distance_km,
            "zenith_angle_deg": zenith_angle_deg,
            "weather_factor": weather_factor,
        }
    }