# simulation/lunar_ring.py

import math
from constants.physical_constants import MOON_RADIUS_KM

class LunarRing:
    def __init__(self, width_km: float):
        self.width_km = width_km

    def calculate_area(self):
        circumference = 2 * math.pi * MOON_RADIUS_KM
        area_km2 = circumference * self.width_km
        return area_km2 * 1e6  # convert to m²