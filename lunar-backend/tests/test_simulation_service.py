"""
Tests for the simulation service orchestration.
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from models.request import SimulationRequest
from services.simulation_service import run_simulation, generate_time_series


class TestRunSimulation:
    """Test suite for the main simulation orchestrator."""

    def test_run_simulation_returns_response(self):
        """Test that run_simulation returns a valid response."""
        request = SimulationRequest(
            ring_width_km=50,
            panel_efficiency=0.22,
            transmission_type="microwave",
            num_ground_stations=5,
            simulation_hours=24
        )
        
        result = run_simulation(request)
        
        assert result is not None
        assert result.total_energy_generated_gw > 0
        assert result.energy_received_gw > 0

    def test_simulation_with_laser(self):
        """Test simulation with laser transmission."""
        request = SimulationRequest(
            ring_width_km=100,
            panel_efficiency=0.30,
            transmission_type="laser",
            num_ground_stations=10,
            simulation_hours=48
        )
        
        result = run_simulation(request)
        
        assert result.transmission_loss_percent > 25  # Laser has higher loss

    def test_simulation_efficiency_calculation(self):
        """Test that efficiency is calculated correctly."""
        request = SimulationRequest(
            ring_width_km=50,
            panel_efficiency=0.22,
            transmission_type="microwave",
            num_ground_stations=5,
            simulation_hours=24
        )
        
        result = run_simulation(request)
        
        expected_efficiency = result.energy_received_gw / result.total_energy_generated_gw
        assert abs(result.system_efficiency - expected_efficiency) < 0.001

    def test_station_distribution(self):
        """Test that energy is distributed across stations."""
        request = SimulationRequest(
            ring_width_km=50,
            panel_efficiency=0.22,
            transmission_type="microwave",
            num_ground_stations=5,
            simulation_hours=24
        )
        
        result = run_simulation(request)
        
        # Check correct number of stations
        assert len(result.stations) == 5
        
        # Check total distributed equals received
        total_distributed = sum(s.received_gw for s in result.stations)
        assert abs(total_distributed - result.energy_received_gw) < 0.01


class TestGenerateTimeSeries:
    """Test suite for time series generation."""

    def test_time_series_length(self):
        """Test that time series has correct length."""
        request = SimulationRequest(
            ring_width_km=50,
            panel_efficiency=0.22,
            transmission_type="microwave",
            num_ground_stations=5,
            simulation_hours=24
        )
        
        time_series = generate_time_series(request, 1000)
        
        assert len(time_series) == 24

    def test_time_series_hours_sequential(self):
        """Test that time series hours are sequential."""
        request = SimulationRequest(
            ring_width_km=50,
            panel_efficiency=0.22,
            transmission_type="microwave",
            num_ground_stations=5,
            simulation_hours=10
        )
        
        time_series = generate_time_series(request, 1000)
        
        for i, point in enumerate(time_series):
            assert point.time_hour == i

    def test_time_series_variation(self):
        """Test that time series has variation (not all same values)."""
        request = SimulationRequest(
            ring_width_km=50,
            panel_efficiency=0.22,
            transmission_type="microwave",
            num_ground_stations=5,
            simulation_hours=100
        )
        
        time_series = generate_time_series(request, 1000)
        
        # Get all generated values
        generated_values = [p.energy_generated_gw for p in time_series]
        
        # Should have some variation (not all identical)
        assert len(set(generated_values)) > 1

    def test_time_series_within_bounds(self):
        """Test that time series values are within expected bounds."""
        request = SimulationRequest(
            ring_width_km=50,
            panel_efficiency=0.22,
            transmission_type="microwave",
            num_ground_stations=5,
            simulation_hours=100
        )
        base_energy = 1000
        
        time_series = generate_time_series(request, base_energy)
        
        for point in time_series:
            # Should be within ±5% of base
            assert point.energy_generated_gw >= base_energy * 0.95
            assert point.energy_generated_gw <= base_energy * 1.05
            # Received should be less than generated
            assert point.energy_received_gw < point.energy_generated_gw
