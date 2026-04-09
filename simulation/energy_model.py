# simulation/energy_model.py

from constants.physical_constants import SOLAR_IRRADIANCE

class EnergyModel:
    def __init__(self, efficiency: float):
        self.efficiency = efficiency

    def generate(self, area_m2: float):
        return area_m2 * SOLAR_IRRADIANCE * self.efficiency