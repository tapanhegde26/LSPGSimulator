"""
Tests for the transmission model calculations.
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.transmission_model import calculate_transmission
from utils.constants import MICROWAVE_BASE_LOSS, LASER_BASE_LOSS, ATMOSPHERIC_LOSS


class TestCalculateTransmission:
    """Test suite for transmission calculation function."""

    def test_microwave_transmission(self):
        """Test microwave transmission calculation."""
        energy_gw = 1000
        
        received, loss_percent = calculate_transmission(energy_gw, "microwave")
        
        # Check received energy is less than input
        assert received < energy_gw
        assert received > 0
        
        # Check loss percentage is positive
        assert loss_percent > 0
        assert loss_percent < 100

    def test_laser_transmission(self):
        """Test laser transmission calculation."""
        energy_gw = 1000
        
        received, loss_percent = calculate_transmission(energy_gw, "laser")
        
        # Check received energy is less than input
        assert received < energy_gw
        assert received > 0
        
        # Laser should have higher loss than microwave
        _, microwave_loss = calculate_transmission(energy_gw, "microwave")
        assert loss_percent > microwave_loss

    def test_microwave_loss_calculation(self):
        """Test that microwave loss matches expected formula."""
        energy_gw = 1000
        expected_loss = MICROWAVE_BASE_LOSS + ATMOSPHERIC_LOSS
        expected_received = energy_gw * (1 - expected_loss)
        
        received, loss_percent = calculate_transmission(energy_gw, "microwave")
        
        assert abs(received - expected_received) < 0.01
        assert abs(loss_percent - expected_loss * 100) < 0.01

    def test_laser_loss_calculation(self):
        """Test that laser loss matches expected formula."""
        energy_gw = 1000
        expected_loss = LASER_BASE_LOSS + ATMOSPHERIC_LOSS
        expected_received = energy_gw * (1 - expected_loss)
        
        received, loss_percent = calculate_transmission(energy_gw, "laser")
        
        assert abs(received - expected_received) < 0.01
        assert abs(loss_percent - expected_loss * 100) < 0.01

    def test_invalid_transmission_type(self):
        """Test that invalid transmission type raises error."""
        with pytest.raises(ValueError, match="Invalid transmission type"):
            calculate_transmission(1000, "invalid")

    def test_zero_energy_input(self):
        """Test transmission with zero energy input."""
        received, loss_percent = calculate_transmission(0, "microwave")
        
        assert received == 0
        # Loss percentage should still be calculated
        assert loss_percent > 0

    def test_energy_conservation(self):
        """Test that received + lost = input energy."""
        energy_gw = 1000
        
        received, loss_percent = calculate_transmission(energy_gw, "microwave")
        lost = energy_gw * (loss_percent / 100)
        
        assert abs(received + lost - energy_gw) < 0.01

    def test_large_energy_values(self):
        """Test with very large energy values."""
        energy_gw = 1_000_000  # 1 million GW
        
        received, loss_percent = calculate_transmission(energy_gw, "microwave")
        
        assert received > 0
        assert received < energy_gw
        assert loss_percent > 0
        assert loss_percent < 100
