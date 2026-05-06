"""
Parameter Optimization Service using Optuna
Finds optimal simulation parameters to maximize energy output.
"""
import optuna
from typing import Dict, Optional, Literal
from dataclasses import dataclass

from services.energy_model import calculate_energy
from services.transmission_model import calculate_transmission
from utils.logger import logger


@dataclass
class OptimizationConstraints:
    """Constraints for parameter optimization."""
    min_ring_width_km: float = 10
    max_ring_width_km: float = 300
    min_efficiency: float = 0.15
    max_efficiency: float = 0.40
    min_stations: int = 3
    max_stations: int = 20
    budget_constraint: Optional[float] = None  # Max cost in arbitrary units


def estimate_cost(
    ring_width_km: float,
    panel_efficiency: float,
    num_stations: int,
    transmission_type: str,
) -> float:
    """
    Estimate construction/operation cost for a configuration.
    
    Cost model (simplified):
    - Ring cost: proportional to area
    - Efficiency cost: exponential (higher efficiency = much more expensive)
    - Station cost: linear per station
    - Laser transmission: more expensive than microwave
    """
    # Base costs (arbitrary units)
    ring_cost_per_km = 100
    station_cost = 500
    
    # Ring cost (proportional to width)
    ring_cost = ring_width_km * ring_cost_per_km
    
    # Efficiency cost (exponential - high efficiency panels are expensive)
    efficiency_cost = 1000 * (2 ** ((panel_efficiency - 0.20) / 0.05))
    
    # Station cost
    stations_cost = num_stations * station_cost
    
    # Transmission type cost
    transmission_cost = 2000 if transmission_type == "laser" else 1000
    
    return ring_cost + efficiency_cost + stations_cost + transmission_cost


def optimize_parameters(
    target_energy_gw: Optional[float] = None,
    constraints: Optional[OptimizationConstraints] = None,
    n_trials: int = 100,
    optimization_goal: Literal["maximize_energy", "maximize_efficiency", "minimize_cost"] = "maximize_energy",
) -> Dict:
    """
    Find optimal simulation parameters using Optuna.
    
    Args:
        target_energy_gw: Target energy output (for cost optimization)
        constraints: Parameter constraints
        n_trials: Number of optimization trials
        optimization_goal: What to optimize for
        
    Returns:
        Dictionary with optimal parameters and predicted results
    """
    if constraints is None:
        constraints = OptimizationConstraints()
    
    logger.info(f"Starting optimization with goal: {optimization_goal}")
    
    def objective(trial: optuna.Trial) -> float:
        # Sample parameters
        ring_width = trial.suggest_float(
            "ring_width_km",
            constraints.min_ring_width_km,
            constraints.max_ring_width_km,
        )
        efficiency = trial.suggest_float(
            "panel_efficiency",
            constraints.min_efficiency,
            constraints.max_efficiency,
        )
        num_stations = trial.suggest_int(
            "num_ground_stations",
            constraints.min_stations,
            constraints.max_stations,
        )
        transmission_type = trial.suggest_categorical(
            "transmission_type",
            ["microwave", "laser"],
        )
        
        # Calculate energy
        generated = calculate_energy(ring_width, efficiency)
        received, loss = calculate_transmission(generated, transmission_type)
        system_efficiency = received / generated if generated > 0 else 0
        
        # Calculate cost
        cost = estimate_cost(ring_width, efficiency, num_stations, transmission_type)
        
        # Check budget constraint
        if constraints.budget_constraint and cost > constraints.budget_constraint:
            return float('inf') if optimization_goal != "minimize_cost" else cost * 10
        
        # Return objective based on goal
        if optimization_goal == "maximize_energy":
            return -received  # Negative because Optuna minimizes
        elif optimization_goal == "maximize_efficiency":
            return -system_efficiency
        else:  # minimize_cost
            # Only consider if we meet target energy
            if target_energy_gw and received < target_energy_gw:
                return cost * 10  # Penalty for not meeting target
            return cost
    
    # Create and run study
    study = optuna.create_study(
        direction="minimize",
        sampler=optuna.samplers.TPESampler(seed=42),
    )
    
    # Suppress Optuna logging
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    
    study.optimize(objective, n_trials=n_trials, show_progress_bar=False)
    
    # Get best parameters
    best_params = study.best_params
    
    # Calculate results with best parameters
    best_generated = calculate_energy(
        best_params["ring_width_km"],
        best_params["panel_efficiency"],
    )
    best_received, best_loss = calculate_transmission(
        best_generated,
        best_params["transmission_type"],
    )
    best_cost = estimate_cost(
        best_params["ring_width_km"],
        best_params["panel_efficiency"],
        best_params["num_ground_stations"],
        best_params["transmission_type"],
    )
    
    # Calculate improvement over baseline
    baseline_generated = calculate_energy(50, 0.22)
    baseline_received, _ = calculate_transmission(baseline_generated, "microwave")
    improvement = ((best_received - baseline_received) / baseline_received) * 100
    
    logger.info(f"Optimization complete. Best energy: {best_received:.2f} GW")
    
    return {
        "optimal_ring_width_km": round(best_params["ring_width_km"], 1),
        "optimal_efficiency": round(best_params["panel_efficiency"], 3),
        "optimal_stations": best_params["num_ground_stations"],
        "optimal_transmission_type": best_params["transmission_type"],
        "predicted_energy_gw": round(best_received, 2),
        "predicted_loss_percent": round(best_loss, 1),
        "estimated_cost": round(best_cost, 0),
        "improvement_percent": round(improvement, 1),
        "optimization_goal": optimization_goal,
        "trials_completed": n_trials,
    }


def quick_optimize(current_params: Dict) -> Dict:
    """
    Quick optimization based on current parameters.
    Suggests improvements without full optimization.
    
    Args:
        current_params: Current simulation parameters
        
    Returns:
        Dictionary with suggestions
    """
    suggestions = []
    
    ring_width = current_params.get("ring_width_km", 50)
    efficiency = current_params.get("panel_efficiency", 0.22)
    transmission = current_params.get("transmission_type", "microwave")
    stations = current_params.get("num_ground_stations", 5)
    
    # Analyze current configuration
    current_generated = calculate_energy(ring_width, efficiency)
    current_received, current_loss = calculate_transmission(current_generated, transmission)
    
    # Suggest improvements
    if ring_width < 100:
        new_generated = calculate_energy(ring_width * 1.5, efficiency)
        new_received, _ = calculate_transmission(new_generated, transmission)
        improvement = ((new_received - current_received) / current_received) * 100
        suggestions.append({
            "parameter": "ring_width_km",
            "current": ring_width,
            "suggested": round(ring_width * 1.5, 0),
            "improvement_percent": round(improvement, 1),
            "reason": "Increasing ring width provides linear energy gains",
        })
    
    if efficiency < 0.30:
        new_generated = calculate_energy(ring_width, min(efficiency * 1.2, 0.35))
        new_received, _ = calculate_transmission(new_generated, transmission)
        improvement = ((new_received - current_received) / current_received) * 100
        suggestions.append({
            "parameter": "panel_efficiency",
            "current": efficiency,
            "suggested": round(min(efficiency * 1.2, 0.35), 2),
            "improvement_percent": round(improvement, 1),
            "reason": "Higher efficiency panels increase output proportionally",
        })
    
    if transmission == "laser":
        new_received, new_loss = calculate_transmission(current_generated, "microwave")
        improvement = ((new_received - current_received) / current_received) * 100
        suggestions.append({
            "parameter": "transmission_type",
            "current": transmission,
            "suggested": "microwave",
            "improvement_percent": round(improvement, 1),
            "reason": "Microwave transmission has lower losses than laser",
        })
    
    if stations < 5:
        suggestions.append({
            "parameter": "num_ground_stations",
            "current": stations,
            "suggested": 5,
            "improvement_percent": 0,
            "reason": "More stations improve reliability and distribution",
        })
    
    return {
        "current_energy_gw": round(current_received, 2),
        "suggestions": suggestions,
        "potential_improvement_percent": sum(s["improvement_percent"] for s in suggestions),
    }
