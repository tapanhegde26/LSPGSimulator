import axios from "axios";

export type SimulationInput = {
  ring_width_km: number;
  panel_efficiency: number;
  transmission_type: "microwave" | "laser";
  num_ground_stations: number;
};

export type SimulationOutput = {
  total_energy_generated_gw: number;
  energy_received_gw: number;
  transmission_loss_percent: number;
  system_efficiency: number;
};

const API_URL = "http://127.0.0.1:8000";

export const runSimulation = async (
  data: SimulationInput,
): Promise<SimulationOutput> => {
  const response = await axios.post(`${API_URL}/simulate`, data);
  return response.data;
};
