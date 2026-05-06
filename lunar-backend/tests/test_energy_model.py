"""
Tests for the energy model calculations.
"""
import pytest
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.energy_model import calculate_energy
from utils.constants import SOLAR_CONSTANT, MOON_RADIUS_KM, PANEL_DEGRADATION


class TestCalculateEnergy:
    """Test suite for energy calculation function."""

    def test_basic_calculation(self):
        """Test basic energy calculation with typical values."""
        ring_width_km = 50
        efficiency = 0.22
        
        result = calculate_energy(ring_width_km, efficiency)
        
        # Result should be positive
        assert result > 0
        # Result should be in reasonable GW range
        assert result > 100  # At least 100 GW for 50km ring
        assert result < 100000  # Less than 100,000 GW

    def test_energy_scales_with_ring_width(self):
        """Test that energy scales linearly with ring width."""
        efficiency = 0.22
        
        energy_50km = calculate_energy(50, efficiency)
        energy_100km = calculate_energy(100, efficiency)
        
        # Doubling ring width should double energy
        assert abs(energy_100km / energy_50km - 2.0) < 0.01

    def test_energy_scales_with_efficiency(self):
        """Test that energy scales linearly with panel efficiency."""
        ring_width_km = 50
        
        energy_20pct = calculate_energy(ring_width_km, 0.20)
        energy_40pct = calculate_energy(ring_width_km, 0.40)
        
        # Doubling efficiency should double energy
        assert abs(energy_40pct / energy_20pct - 2.0) < 0.01

    def test_formula_correctness(self):
        """Test that the formula produces expected results."""
        ring_width_km = 100
        efficiency = 0.25
        
        # Manual calculation
        circumference_km = 2 * math.pi * MOON_RADIUS_KM
        area_km2 = circumference_km * ring_width_km
        area_m2 = area_km2 * 1e6
        expected_watts = area_m2 * SOLAR_CONSTANT * efficiency * PANEL_DEGRADATION
        expected_gw = expected_watts / 1e9
        
        result = calculate_energy(ring_width_km, efficiency)
        
        assert abs(result - expected_gw) < 0.01

    def test_zero_width_returns_zero(self):
        """Test that zero ring width returns zero energy."""
        result = calculate_energy(0, 0.22)
        assert result == 0

    def test_zero_efficiency_returns_zero(self):
        """Test that zero efficiency returns zero energy."""
        result = calculate_energy(50, 0)
        assert result == 0

    def test_maximum_realistic_values(self):
        """Test with maximum realistic parameter values."""
        # Maximum ring width (500km) and efficiency (50%)
        result = calculate_energy(500, 0.50)
        
        # Should produce very large but finite result
        assert result > 0
        assert result < float('inf')
        assert result > 10000  # Should be at least 10,000 GW

    def test_small_values(self):
        """Test with very small parameter values."""
        result = calculate_energy(1, 0.05)
        
        # Should still produce positive result
        assert result > 0
        assert result < 100  # Should be relatively small
