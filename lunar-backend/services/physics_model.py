"""
Advanced Physics Models for Lunar Solar Simulator
Includes lunar day/night cycle, atmospheric effects, and orbital mechanics.
"""
import math
from typing import Tuple
from utils.constants import MOON_RADIUS_KM


# Physical Constants
LUNAR_DAY_HOURS = 708  # ~29.5 Earth days
EARTH_MOON_DISTANCE_KM = 384400
EARTH_MOON_PERIGEE_KM = 356500  # Closest approach
EARTH_MOON_APOGEE_KM = 406700   # Farthest distance
LUNAR_ORBITAL_PERIOD_HOURS = 655.7  # ~27.3 days (sidereal)

# Atmospheric Constants
EARTH_ATMOSPHERE_HEIGHT_KM = 100  # Karman line
SEA_LEVEL_PRESSURE_PA = 101325
SCALE_HEIGHT_KM = 8.5  # Atmospheric scale height


def calculate_solar_exposure(lunar_day_hour: float) -> float:
    """
    Calculate solar exposure factor based on lunar rotation.
    
    The Moon rotates once every ~29.5 Earth days (708 hours).
    At any point on the lunar equator, there's ~14.75 days of sunlight
    followed by ~14.75 days of darkness.
    
    Args:
        lunar_day_hour: Current hour in the lunar day cycle (0-708)
        
    Returns:
        Solar exposure factor (0.0 to 1.0)
        - 1.0 = Full sunlight (lunar noon)
        - 0.0 = Complete darkness (lunar night)
    """
    # Normalize to 0-2π
    angle = (lunar_day_hour / LUNAR_DAY_HOURS) * 2 * math.pi
    
    # Cosine function shifted so 0 = sunrise, π/2 = noon, π = sunset
    # We want noon at hour 177 (quarter of lunar day)
    exposure = math.cos(angle - math.pi / 2)
    
    # Clamp to 0-1 (negative values = night)
    return max(0.0, exposure)


def calculate_ring_average_exposure(ring_width_km: float) -> float:
    """
    Calculate average solar exposure for the entire lunar ring.
    
    Since the ring encircles the Moon's equator, approximately half
    of it is always in sunlight. The actual average depends on the
    ring width and the Sun's angle.
    
    Args:
        ring_width_km: Width of the solar panel ring
        
    Returns:
        Average exposure factor for the entire ring (typically ~0.5)
    """
    # For a ring around the equator, on average half is illuminated
    # This is a simplification - actual value varies slightly with solar angle
    base_exposure = 0.5
    
    # Wider rings have slightly more consistent exposure
    # due to averaging over more area
    width_factor = 1.0 + (ring_width_km / 1000) * 0.02
    
    return min(base_exposure * width_factor, 0.55)


def calculate_earth_moon_distance(orbital_hour: float) -> float:
    """
    Calculate Earth-Moon distance based on orbital position.
    
    The Moon's orbit is elliptical, varying from 356,500 km (perigee)
    to 406,700 km (apogee).
    
    Args:
        orbital_hour: Current hour in the lunar orbital period
        
    Returns:
        Current Earth-Moon distance in kilometers
    """
    # Normalize to 0-2π
    angle = (orbital_hour / LUNAR_ORBITAL_PERIOD_HOURS) * 2 * math.pi
    
    # Semi-major and semi-minor axes
    a = (EARTH_MOON_PERIGEE_KM + EARTH_MOON_APOGEE_KM) / 2
    e = (EARTH_MOON_APOGEE_KM - EARTH_MOON_PERIGEE_KM) / (EARTH_MOON_APOGEE_KM + EARTH_MOON_PERIGEE_KM)
    
    # Distance using orbital mechanics (simplified)
    distance = a * (1 - e * math.cos(angle))
    
    return distance


def calculate_beam_spreading_loss(
    distance_km: float,
    transmission_type: str,
    antenna_diameter_m: float = 1000
) -> float:
    """
    Calculate energy loss due to beam spreading over distance.
    
    Uses the inverse square law with corrections for antenna/laser focusing.
    
    Args:
        distance_km: Transmission distance in kilometers
        transmission_type: 'microwave' or 'laser'
        antenna_diameter_m: Diameter of transmitting antenna/aperture
        
    Returns:
        Beam spreading loss factor (0.0 to 1.0, where 1.0 = no loss)
    """
    distance_m = distance_km * 1000
    
    if transmission_type == "microwave":
        # Microwave beam spreading
        # Using 2.45 GHz frequency (common for power transmission)
        wavelength_m = 0.122  # ~12.2 cm
        
        # Antenna gain (simplified)
        gain = (math.pi * antenna_diameter_m / wavelength_m) ** 2
        
        # Free space path loss
        fspl = (4 * math.pi * distance_m / wavelength_m) ** 2
        
        # Effective loss considering antenna gain
        loss_factor = gain / fspl
        
    else:  # laser
        # Laser beam divergence
        # Assuming 1 micron wavelength infrared laser
        wavelength_m = 1e-6
        
        # Beam divergence angle (diffraction limited)
        divergence = wavelength_m / (math.pi * antenna_diameter_m / 2)
        
        # Beam diameter at target
        beam_diameter = antenna_diameter_m + 2 * distance_m * math.tan(divergence)
        
        # Assuming 10km diameter receiver
        receiver_diameter = 10000
        
        # Fraction of beam captured
        loss_factor = min(1.0, (receiver_diameter / beam_diameter) ** 2)
    
    return min(1.0, max(0.01, loss_factor))


def calculate_atmospheric_absorption(
    zenith_angle_deg: float,
    weather_factor: float = 1.0,
    transmission_type: str = "microwave"
) -> Tuple[float, float]:
    """
    Calculate atmospheric absorption for energy beam.
    
    Accounts for:
    - Path length through atmosphere (depends on zenith angle)
    - Weather conditions (clouds, rain, humidity)
    - Transmission type (microwave vs laser)
    
    Args:
        zenith_angle_deg: Angle from vertical (0 = directly overhead)
        weather_factor: Weather impact (1.0 = clear, 0.5 = cloudy, 0.2 = heavy rain)
        transmission_type: 'microwave' or 'laser'
        
    Returns:
        Tuple of (transmission_factor, loss_percentage)
    """
    # Air mass factor (path length through atmosphere)
    # Using Kasten-Young formula approximation
    zenith_rad = math.radians(min(zenith_angle_deg, 85))  # Cap at 85 degrees
    air_mass = 1 / (math.cos(zenith_rad) + 0.50572 * (96.07995 - zenith_angle_deg) ** -1.6364)
    
    if transmission_type == "microwave":
        # Microwave absorption coefficients
        # Water vapor is main absorber at 2.45 GHz
        base_absorption = 0.01  # ~1% per air mass in clear conditions
        rain_absorption = 0.15  # Additional absorption in rain
        
        total_absorption = base_absorption * air_mass
        if weather_factor < 0.8:  # Rainy conditions
            total_absorption += rain_absorption * (1 - weather_factor) * air_mass
            
    else:  # laser
        # Laser absorption (more sensitive to weather)
        base_absorption = 0.02  # ~2% per air mass in clear conditions
        cloud_absorption = 0.40  # Significant absorption in clouds
        
        total_absorption = base_absorption * air_mass
        if weather_factor < 1.0:
            total_absorption += cloud_absorption * (1 - weather_factor) * air_mass
    
    transmission_factor = math.exp(-total_absorption)
    loss_percentage = (1 - transmission_factor) * 100
    
    return transmission_factor, loss_percentage


def calculate_panel_temperature_efficiency(
    solar_intensity_factor: float,
    base_efficiency: float
) -> float:
    """
    Calculate panel efficiency accounting for temperature effects.
    
    Solar panels lose efficiency at high temperatures. In space,
    panels can get very hot in direct sunlight.
    
    Args:
        solar_intensity_factor: Solar intensity (1.0 = full sun)
        base_efficiency: Panel efficiency at standard test conditions
        
    Returns:
        Adjusted efficiency accounting for temperature
    """
    # Standard test conditions: 25°C
    # In space with full sun, panels can reach 60-80°C
    # Efficiency drops ~0.4% per degree C above 25°C
    
    # Estimate panel temperature based on solar intensity
    # Simplified thermal model
    ambient_space_temp = -270  # Deep space background
    max_sun_temp = 80  # Maximum temperature in full sun
    
    panel_temp = ambient_space_temp + (max_sun_temp - ambient_space_temp) * solar_intensity_factor
    panel_temp = max(panel_temp, -40)  # Minimum operating temp
    
    # Temperature coefficient (typical for silicon cells)
    temp_coefficient = -0.004  # -0.4% per degree C
    
    # Efficiency adjustment
    temp_adjustment = 1 + temp_coefficient * (panel_temp - 25)
    
    return base_efficiency * max(0.7, min(1.1, temp_adjustment))


def calculate_panel_degradation(years_in_operation: float) -> float:
    """
    Calculate panel degradation over time.
    
    Solar panels in space degrade due to:
    - Radiation damage
    - Micrometeorite impacts
    - Thermal cycling
    
    Args:
        years_in_operation: Years since installation
        
    Returns:
        Degradation factor (1.0 = new, decreasing over time)
    """
    # Typical space solar panel degradation: ~2.5% per year
    # Better than Earth due to no weather, but more radiation
    annual_degradation_rate = 0.025
    
    # Exponential decay model
    degradation_factor = math.exp(-annual_degradation_rate * years_in_operation)
    
    # Minimum efficiency floor (panels don't degrade below ~50%)
    return max(0.5, degradation_factor)
