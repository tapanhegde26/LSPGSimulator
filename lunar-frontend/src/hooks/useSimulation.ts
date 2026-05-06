/**
 * Custom hook for managing simulation state and API calls
 */
import { useState, useCallback } from "react";
import { runSimulation } from "../services/api";
import { useWebSocketSimulation } from "./useWebSocketSimulation";
import type { 
  SimulationInput, 
  SimulationResponse, 
  TimeSeriesPoint 
} from "../types";

interface UseSimulationReturn {
  // State
  result: SimulationResponse | null;
  liveData: TimeSeriesPoint[];
  isLoading: boolean;
  isStreaming: boolean;
  error: string | null;
  
  // Actions
  runSimulationWithStreaming: (input: SimulationInput) => Promise<void>;
  runSimulationOnly: (input: SimulationInput) => Promise<void>;
  clearResults: () => void;
}

export function useSimulation(): UseSimulationReturn {
  const [result, setResult] = useState<SimulationResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {
    liveData,
    isStreaming,
    error: wsError,
    startStreaming,
    clearData,
  } = useWebSocketSimulation({
    onError: (err) => setError(err),
  });

  // Run both REST API and WebSocket streaming
  const runSimulationWithStreaming = useCallback(async (input: SimulationInput) => {
    setIsLoading(true);
    setError(null);
    setResult(null);
    clearData();

    try {
      // Start WebSocket streaming for live graph
      startStreaming(input);

      // Call REST API for complete results
      const data = await runSimulation(input);
      setResult(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Simulation failed";
      setError(message);
      console.error("Simulation error:", err);
    } finally {
      setIsLoading(false);
    }
  }, [startStreaming, clearData]);

  // Run only REST API (no streaming)
  const runSimulationOnly = useCallback(async (input: SimulationInput) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await runSimulation(input);
      setResult(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Simulation failed";
      setError(message);
      console.error("Simulation error:", err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearResults = useCallback(() => {
    setResult(null);
    setError(null);
    clearData();
  }, [clearData]);

  return {
    result,
    liveData,
    isLoading,
    isStreaming,
    error: error || wsError,
    runSimulationWithStreaming,
    runSimulationOnly,
    clearResults,
  };
}
