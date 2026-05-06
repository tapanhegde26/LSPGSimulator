"""
Ground Station Optimization Service
Provides algorithms for optimal ground station placement and configuration.
"""
import math
import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class GroundStationLocation:
    """Represents a ground station location."""
    station_id: int
    latitude: float
    longitude: float
    name: str
    elevation_m: float = 0
    weather_factor: float = 0.85  # Average weather conditions


# Pre-defined optimal locations (based on real-world considerations)
OPTIMAL_LOCATIONS = [
    GroundStationLocation(1, 35.0, -120.0, "California Desert", 500, 0.95),
    GroundStationLocation(2, 25.0, -110.0, "Sonoran Desert", 400, 0.92),
    GroundStationLocation(3, -23.5, 134.0, "Australian Outback", 300, 0.90),
    GroundStationLocation(4, 28.5, 77.0, "Rajasthan, India", 250, 0.85),
    GroundStationLocation(5, 31.0, 35.0, "Negev Desert", 500, 0.90),
    GroundStationLocation(6, 23.5, -15.0, "Western Sahara", 200, 0.92),
    GroundStationLocation(7, -24.0, -70.0, "Atacama Desert", 2400, 0.95),
    GroundStationLocation(8, 40.0, 100.0, "Gobi Desert", 1000, 0.88),
    GroundStationLocation(9, -25.0, 25.0, "Kalahari Desert", 1000, 0.87),
    GroundStationLocation(10, 33.0, 44.0, "Arabian Desert", 300, 0.90),
    GroundStationLocation(11, 36.0, 140.0, "Japan", 100, 0.75),
    GroundStationLocation(12, 52.0, 5.0, "Netherlands", 0, 0.70),
    GroundStationLocation(13, -33.0, 151.0, "Sydney Region", 50, 0.80),
    GroundStationLocation(14, 19.0, -99.0, "Mexico City Region", 2200, 0.78),
    GroundStationLocation(15, 1.0, 103.0, "Singapore", 15, 0.72),
]


def get_optimal_station_locations(
    num_stations: int,
    prefer_desert: bool = True,
    latitude_range: Tuple[float, float] = (-60, 60),
) -> List[Dict]:
    """
    Get optimal ground station locations.
    
    Selects locations based on:
    - Weather conditions (desert locations preferred)
    - Geographic distribution (spread across longitudes)
    - Latitude constraints (avoid polar regions)
    
    Args:
        num_stations: Number of stations to select
        prefer_desert: Prioritize desert locations for better weather
        latitude_range: Allowed latitude range
        
    Returns:
        List of station dictionaries with location data
    """
    # Filter by latitude
    valid_locations = [
        loc for loc in OPTIMAL_LOCATIONS
        if latitude_range[0] <= loc.latitude <= latitude_range[1]
    ]
    
    # Sort by weather factor if preferring desert
    if prefer_desert:
        valid_locations.sort(key=lambda x: x.weather_factor, reverse=True)
    
    # Select stations with good geographic distribution
    selected = []
    used_longitudes = []
    
    for loc in valid_locations:
        if len(selected) >= num_stations:
            break
            
        # Check longitude separation (at least 30 degrees apart)
        too_close = any(
            abs(loc.longitude - used_lon) < 30 or 
            abs(loc.longitude - used_lon) > 330
            for used_lon in used_longitudes
        )
        
        if not too_close or len(selected) < num_stations // 2:
            selected.append(loc)
            used_longitudes.append(loc.longitude)
    
    # If we need more stations, add remaining ones
    for loc in valid_locations:
        if len(selected) >= num_stations:
            break
        if loc not in selected:
            selected.append(loc)
    
    # Convert to dictionaries
    return [
        {
            "station_id": i + 1,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "name": loc.name,
            "elevation_m": loc.elevation_m,
            "weather_factor": loc.weather_factor,
        }
        for i, loc in enumerate(selected[:num_stations])
    ]


def calculate_station_visibility(
    station_lat: float,
    station_lon: float,
    moon_declination: float = 0,
) -> Tuple[float, float]:
    """
    Calculate Moon visibility from a ground station.
    
    Args:
        station_lat: Station latitude in degrees
        station_lon: Station longitude in degrees
        moon_declination: Moon's declination (simplified)
        
    Returns:
        Tuple of (visibility_hours_per_day, max_elevation_deg)
    """
    # Simplified visibility calculation
    # Moon is visible roughly 12 hours per day on average
    lat_rad = math.radians(station_lat)
    
    # Maximum elevation depends on latitude and Moon's declination
    max_elevation = 90 - abs(station_lat - moon_declination)
    
    # Visibility hours (simplified)
    if abs(station_lat) > 60:
        visibility_hours = 8  # Reduced at high latitudes
    else:
        visibility_hours = 12
    
    return visibility_hours, max_elevation


def optimize_energy_distribution(
    total_energy_gw: float,
    stations: List[Dict],
    optimization_mode: str = "equal",
) -> List[Dict]:
    """
    Optimize energy distribution across ground stations.
    
    Args:
        total_energy_gw: Total energy to distribute
        stations: List of station dictionaries
        optimization_mode: 'equal', 'weighted', or 'demand'
        
    Returns:
        List of stations with received_gw values
    """
    num_stations = len(stations)
    
    if optimization_mode == "equal":
        # Simple equal distribution
        per_station = total_energy_gw / num_stations
        for station in stations:
            station["received_gw"] = per_station
            
    elif optimization_mode == "weighted":
        # Weight by weather factor
        total_weight = sum(s.get("weather_factor", 0.85) for s in stations)
        for station in stations:
            weight = station.get("weather_factor", 0.85)
            station["received_gw"] = total_energy_gw * (weight / total_weight)
            
    elif optimization_mode == "demand":
        # Placeholder for demand-based distribution
        # Would integrate with actual power grid demand data
        per_station = total_energy_gw / num_stations
        for station in stations:
            station["received_gw"] = per_station
    
    return stations


def calculate_global_coverage(stations: List[Dict]) -> Dict:
    """
    Calculate global coverage statistics for station network.
    
    Args:
        stations: List of station dictionaries
        
    Returns:
        Dictionary with coverage statistics
    """
    if not stations:
        return {"coverage_percent": 0, "avg_distance_km": 0}
    
    lats = [s["latitude"] for s in stations]
    lons = [s["longitude"] for s in stations]
    
    # Calculate coverage metrics
    lat_spread = max(lats) - min(lats)
    
    # Longitude spread (accounting for wrap-around)
    lons_sorted = sorted(lons)
    lon_gaps = []
    for i in range(len(lons_sorted)):
        next_i = (i + 1) % len(lons_sorted)
        gap = lons_sorted[next_i] - lons_sorted[i]
        if gap < 0:
            gap += 360
        lon_gaps.append(gap)
    
    max_lon_gap = max(lon_gaps) if lon_gaps else 360
    
    # Estimate coverage (simplified)
    coverage_percent = min(100, (360 - max_lon_gap) / 360 * 100 * (lat_spread / 120))
    
    return {
        "coverage_percent": round(coverage_percent, 1),
        "latitude_spread_deg": lat_spread,
        "max_longitude_gap_deg": max_lon_gap,
        "num_stations": len(stations),
    }
