"""
Earth Receiver Model for Lunar Solar Simulator
Handles energy distribution to ground stations.
"""
from typing import List, Dict, Optional
from services.station_optimizer import (
    get_optimal_station_locations,
    optimize_energy_distribution,
    calculate_global_coverage,
)


def distribute_energy(
    total_energy: float, 
    stations: int,
    use_optimal_locations: bool = False,
    optimization_mode: str = "equal",
) -> List[Dict]:
    """
    Distribute received energy across ground stations.
    
    Args:
        total_energy: Total energy to distribute in GW
        stations: Number of ground stations
        use_optimal_locations: Use pre-defined optimal locations
        optimization_mode: Distribution strategy ('equal', 'weighted', 'demand')
        
    Returns:
        List of station dictionaries with energy allocation
        
    Raises:
        ValueError: If stations <= 0
    """
    if stations <= 0:
        raise ValueError("Number of stations must be > 0")

    if use_optimal_locations:
        # Get optimal station locations
        station_list = get_optimal_station_locations(stations)
        
        # Distribute energy with optimization
        station_list = optimize_energy_distribution(
            total_energy,
            station_list,
            optimization_mode
        )
        
        return station_list
    else:
        # Simple equal distribution
        per_station = total_energy / stations
        
        return [
            {
                "station_id": i + 1,
                "received_gw": per_station,
            }
            for i in range(stations)
        ]


def get_station_details(num_stations: int) -> Dict:
    """
    Get detailed information about ground station network.
    
    Args:
        num_stations: Number of stations in network
        
    Returns:
        Dictionary with station details and coverage info
    """
    stations = get_optimal_station_locations(num_stations)
    coverage = calculate_global_coverage(stations)
    
    return {
        "stations": stations,
        "coverage": coverage,
        "total_stations": num_stations,
    }