"""
Pytest configuration and fixtures.
"""
import pytest
from fastapi.testclient import TestClient

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def valid_simulation_request():
    """Return a valid simulation request payload."""
    return {
        "ring_width_km": 50,
        "panel_efficiency": 0.22,
        "transmission_type": "microwave",
        "num_ground_stations": 5,
        "simulation_hours": 24
    }


@pytest.fixture
def minimal_simulation_request():
    """Return a minimal valid simulation request."""
    return {
        "ring_width_km": 10,
        "panel_efficiency": 0.1,
        "transmission_type": "laser",
        "num_ground_stations": 1,
        "simulation_hours": 1
    }
