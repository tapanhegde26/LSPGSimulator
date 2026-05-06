"""
Tests for the FastAPI endpoints.
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestHealthEndpoint:
    """Test suite for health check endpoints."""

    def test_root_health_check(self, client):
        """Test the root health check endpoint."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert data["simulation_ready"] is True

    def test_health_endpoint(self, client):
        """Test the /health endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestSimulateEndpoint:
    """Test suite for the simulation endpoint."""

    def test_valid_simulation_request(self, client, valid_simulation_request):
        """Test simulation with valid parameters."""
        response = client.post("/simulate", json=valid_simulation_request)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields exist
        assert "total_energy_generated_gw" in data
        assert "energy_received_gw" in data
        assert "transmission_loss_percent" in data
        assert "system_efficiency" in data
        assert "stations" in data
        assert "time_series" in data
        assert "insights" in data

    def test_simulation_energy_values(self, client, valid_simulation_request):
        """Test that simulation returns sensible energy values."""
        response = client.post("/simulate", json=valid_simulation_request)
        data = response.json()
        
        # Generated energy should be positive
        assert data["total_energy_generated_gw"] > 0
        
        # Received should be less than generated
        assert data["energy_received_gw"] < data["total_energy_generated_gw"]
        assert data["energy_received_gw"] > 0
        
        # Loss should be between 0 and 100
        assert 0 < data["transmission_loss_percent"] < 100
        
        # Efficiency should be between 0 and 1
        assert 0 < data["system_efficiency"] < 1

    def test_simulation_stations(self, client, valid_simulation_request):
        """Test that simulation returns correct number of stations."""
        response = client.post("/simulate", json=valid_simulation_request)
        data = response.json()
        
        assert len(data["stations"]) == valid_simulation_request["num_ground_stations"]
        
        # Each station should have required fields
        for station in data["stations"]:
            assert "station_id" in station
            assert "received_gw" in station
            assert station["received_gw"] > 0

    def test_simulation_time_series(self, client, valid_simulation_request):
        """Test that simulation returns correct time series length."""
        response = client.post("/simulate", json=valid_simulation_request)
        data = response.json()
        
        assert len(data["time_series"]) == valid_simulation_request["simulation_hours"]
        
        # Each point should have required fields
        for point in data["time_series"]:
            assert "time_hour" in point
            assert "energy_generated_gw" in point
            assert "energy_received_gw" in point

    def test_simulation_insights(self, client, valid_simulation_request):
        """Test that simulation returns insights."""
        response = client.post("/simulate", json=valid_simulation_request)
        data = response.json()
        
        # Insights should be a list
        assert isinstance(data["insights"], list)

    def test_minimal_simulation(self, client, minimal_simulation_request):
        """Test simulation with minimal valid parameters."""
        response = client.post("/simulate", json=minimal_simulation_request)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_energy_generated_gw"] > 0

    def test_microwave_vs_laser(self, client, valid_simulation_request):
        """Test that laser has higher loss than microwave."""
        # Test microwave
        valid_simulation_request["transmission_type"] = "microwave"
        response_mw = client.post("/simulate", json=valid_simulation_request)
        data_mw = response_mw.json()
        
        # Test laser
        valid_simulation_request["transmission_type"] = "laser"
        response_laser = client.post("/simulate", json=valid_simulation_request)
        data_laser = response_laser.json()
        
        # Laser should have higher loss
        assert data_laser["transmission_loss_percent"] > data_mw["transmission_loss_percent"]

    def test_invalid_transmission_type(self, client, valid_simulation_request):
        """Test that invalid transmission type returns error."""
        valid_simulation_request["transmission_type"] = "invalid"
        response = client.post("/simulate", json=valid_simulation_request)
        
        assert response.status_code == 422  # Validation error

    def test_negative_ring_width(self, client, valid_simulation_request):
        """Test that negative ring width returns error."""
        valid_simulation_request["ring_width_km"] = -10
        response = client.post("/simulate", json=valid_simulation_request)
        
        assert response.status_code == 422

    def test_efficiency_out_of_range(self, client, valid_simulation_request):
        """Test that efficiency > 1 returns error."""
        valid_simulation_request["panel_efficiency"] = 1.5
        response = client.post("/simulate", json=valid_simulation_request)
        
        assert response.status_code == 422

    def test_zero_ground_stations(self, client, valid_simulation_request):
        """Test that zero ground stations returns error."""
        valid_simulation_request["num_ground_stations"] = 0
        response = client.post("/simulate", json=valid_simulation_request)
        
        assert response.status_code == 422

    def test_simulation_hours_limit(self, client, valid_simulation_request):
        """Test that simulation hours over limit returns error."""
        valid_simulation_request["simulation_hours"] = 1000  # Over 168 limit
        response = client.post("/simulate", json=valid_simulation_request)
        
        assert response.status_code == 422


class TestAPIDocumentation:
    """Test suite for API documentation endpoints."""

    def test_openapi_schema(self, client):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")
        
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "paths" in data

    def test_docs_endpoint(self, client):
        """Test that Swagger docs are available."""
        response = client.get("/docs")
        
        assert response.status_code == 200

    def test_redoc_endpoint(self, client):
        """Test that ReDoc is available."""
        response = client.get("/redoc")
        
        assert response.status_code == 200
