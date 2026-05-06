/**
 * Type definitions for the Lunar Solar Simulator
 */

// Transmission types
export type TransmissionType = "microwave" | "laser";

// Simulation input parameters
export interface SimulationInput {
  ring_width_km: number;
  panel_efficiency: number;
  transmission_type: TransmissionType;
  num_ground_stations: number;
  simulation_hours: number;
  // Advanced options (Phase 2)
  include_lunar_cycle?: boolean;
  include_atmospheric_effects?: boolean;
  lunar_day_hour?: number;
}

// Time series data point
export interface TimeSeriesPoint {
  time_hour: number;
  energy_generated_gw: number;
  energy_received_gw: number;
  solar_exposure?: number;
  atmospheric_loss?: number;
}

// Ground station data
export interface GroundStation {
  station_id: number;
  received_gw: number;
  latitude?: number;
  longitude?: number;
  name?: string;
}

// Optimization result
export interface OptimizationResult {
  optimal_ring_width_km: number;
  optimal_efficiency: number;
  optimal_stations: number;
  optimal_transmission_type: TransmissionType;
  predicted_energy_gw: number;
  improvement_percent: number;
}

// Complete simulation response
export interface SimulationResponse {
  total_energy_generated_gw: number;
  energy_received_gw: number;
  transmission_loss_percent: number;
  system_efficiency: number;
  stations: GroundStation[];
  time_series: TimeSeriesPoint[];
  insights: string[];
  optimization?: OptimizationResult;
}

// WebSocket message types
export interface WebSocketTimeSeriesMessage {
  time_hour: number;
  energy_generated_gw: number;
  energy_received_gw: number;
  transmission_loss_percent?: number;
}

export interface WebSocketCompleteMessage {
  status: "complete";
  total_hours: number;
}

export interface WebSocketErrorMessage {
  error: string;
}

export type WebSocketMessage = 
  | WebSocketTimeSeriesMessage 
  | WebSocketCompleteMessage 
  | WebSocketErrorMessage;

// Health check response
export interface HealthResponse {
  status: string;
  version: string;
  simulation_ready: boolean;
}

// Scenario for comparison feature
export interface Scenario {
  id: string;
  name: string;
  params: SimulationInput;
  results: SimulationResponse | null;
  createdAt: Date;
}

// Export format options
export type ExportFormat = "pdf" | "csv" | "json";

export interface ExportOptions {
  format: ExportFormat;
  includeGraphs: boolean;
  includeInsights: boolean;
}

// UI State types
export interface SimulationState {
  isLoading: boolean;
  isStreaming: boolean;
  error: string | null;
  result: SimulationResponse | null;
  liveData: TimeSeriesPoint[];
}

// Form validation
export interface ValidationError {
  field: keyof SimulationInput;
  message: string;
}

// Default values
export const DEFAULT_SIMULATION_INPUT: SimulationInput = {
  ring_width_km: 50,
  panel_efficiency: 0.22,
  transmission_type: "microwave",
  num_ground_stations: 5,
  simulation_hours: 24,
  include_lunar_cycle: false,
  include_atmospheric_effects: false,
  lunar_day_hour: 354,
};

// Validation constraints
export const VALIDATION_CONSTRAINTS = {
  ring_width_km: { min: 1, max: 500 },
  panel_efficiency: { min: 0.05, max: 0.50 },
  num_ground_stations: { min: 1, max: 50 },
  simulation_hours: { min: 1, max: 168 },
  lunar_day_hour: { min: 0, max: 708 },
} as const;
