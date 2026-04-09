# simulation/transmission.py

import math
from constants.physical_constants import EARTH_MOON_DISTANCE_KM

class TransmissionModel:
    def __init__(self, transmission_type: str):
        self.transmission_type = transmission_type

    def transmit(self, energy):
        if self.transmission_type == "microwave":
            k = 0.0000001
        else:  # laser
            k = 0.0000002

        return energy * math.exp(-k * EARTH_MOON_DISTANCE_KM)