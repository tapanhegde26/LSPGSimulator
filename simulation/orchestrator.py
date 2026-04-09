# simulation/orchestrator.py

from simulation.lunar_ring import LunarRing
from simulation.energy_model import EnergyModel
from simulation.transmission_model import TransmissionModel
from simulation.earth_receiver import EarthReceiver
from utils.logger import get_logger

logger = get_logger(__name__)

class Simulation:
    def run(self, input_data):
        try:
            logger.info("Simulation started")
            ring = LunarRing(input_data.ring_width_km)
            area = ring.calculate_area()
            logger.info(f"Calculated area: {area}")

            energy_model = EnergyModel(input_data.panel_efficiency)
            generated = energy_model.generate(area)
            logger.info(f"Generated energy: {generated}")

            transmission = TransmissionModel(input_data.transmission_type)
            transmitted = transmission.transmit(generated)
            logger.info(f"Transmitted energy: {transmitted}")

            receiver = EarthReceiver(input_data.num_ground_stations)
            received = receiver.receive(transmitted)
            logger.info(f"Received energy: {received}")

            loss = (generated - received) / generated
            
            logger.info("Simulation completed")

            return {
                "total_energy_generated_gw": generated / 1e9,
                "energy_received_gw": received / 1e9,
                "transmission_loss_percent": loss * 100,
                "system_efficiency": received / generated
            }
        except Exception as e:
            logger.error(f"Simulation failed: {str(e)}")
        raise