/**
 * API Service for Lunar Solar Simulator
 */
import axios, { AxiosError } from "axios";
import { API_CONFIG, ENDPOINTS } from "../config/api";
import type { 
  SimulationInput, 
  SimulationResponse, 
  HealthResponse,
  OptimizationResult,
  ExportOptions 
} from "../types";

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_CONFIG.baseUrl,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000, // 30 second timeout
});

// Error handler
const handleApiError = (error: unknown): never => {
  if (error instanceof AxiosError) {
    if (error.response) {
      // Server responded with error
      const message = error.response.data?.detail || error.response.statusText;
      throw new Error(`API Error: ${message}`);
    } else if (error.request) {
      // Request made but no response
      throw new Error("No response from server. Please check if the backend is running.");
    }
  }
  throw error;
};

/**
 * Check API health status
 */
export const checkHealth = async (): Promise<HealthResponse> => {
  try {
    const response = await apiClient.get<HealthResponse>(ENDPOINTS.health);
    return response.data;
  } catch (error) {
    return handleApiError(error);
  }
};

/**
 * Run a complete simulation
 */
export const runSimulation = async (
  data: SimulationInput
): Promise<SimulationResponse> => {
  try {
    const response = await apiClient.post<SimulationResponse>(
      ENDPOINTS.simulate, 
      data
    );
    return response.data;
  } catch (error) {
    return handleApiError(error);
  }
};

/**
 * Run parameter optimization (Phase 4)
 */
export const runOptimization = async (
  targetEnergyGw: number,
  budgetConstraint?: number
): Promise<OptimizationResult> => {
  try {
    const response = await apiClient.post<OptimizationResult>(
      ENDPOINTS.optimize,
      { target_energy_gw: targetEnergyGw, budget_constraint: budgetConstraint }
    );
    return response.data;
  } catch (error) {
    return handleApiError(error);
  }
};

/**
 * Export simulation results (Phase 4)
 */
export const exportResults = async (
  simulationId: string,
  options: ExportOptions
): Promise<Blob> => {
  try {
    const response = await apiClient.post(
      `${ENDPOINTS.export}/${simulationId}`,
      options,
      { responseType: "blob" }
    );
    return response.data;
  } catch (error) {
    return handleApiError(error);
  }
};

