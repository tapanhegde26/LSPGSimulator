# simulation/earth_receiver.py

class EarthReceiver:
    def __init__(self, num_stations: int):
        self.num_stations = num_stations

    def receive(self, energy):
        efficiency = 0.9  # conversion efficiency
        return energy * efficiency