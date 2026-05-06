/**
 * Custom hook for WebSocket simulation streaming
 */
import { useState, useCallback, useRef, useEffect } from "react";
import { getWsUrl, ENDPOINTS } from "../config/api";
import type { 
  SimulationInput, 
  TimeSeriesPoint, 
  WebSocketMessage 
} from "../types";

interface UseWebSocketSimulationOptions {
  onComplete?: () => void;
  onError?: (error: string) => void;
}

interface UseWebSocketSimulationReturn {
  liveData: TimeSeriesPoint[];
  isStreaming: boolean;
  error: string | null;
  startStreaming: (input: SimulationInput) => void;
  stopStreaming: () => void;
  clearData: () => void;
}

export function useWebSocketSimulation(
  options: UseWebSocketSimulationOptions = {}
): UseWebSocketSimulationReturn {
  const { onComplete, onError } = options;
  
  const [liveData, setLiveData] = useState<TimeSeriesPoint[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const wsRef = useRef<WebSocket | null>(null);

  // Cleanup WebSocket on unmount
  useEffect(() => {
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, []);

  const startStreaming = useCallback((input: SimulationInput) => {
    // Close existing connection if any
    if (wsRef.current) {
      wsRef.current.close();
    }

    setLiveData([]);
    setError(null);
    setIsStreaming(true);

    const ws = new WebSocket(getWsUrl(ENDPOINTS.wsSimulate));
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("WebSocket connected");
      ws.send(JSON.stringify(input));
    };

    ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data);
        
        // Check if it's a completion message
        if ("status" in message && message.status === "complete") {
          setIsStreaming(false);
          onComplete?.();
          return;
        }
        
        // Check if it's an error message
        if ("error" in message) {
          setError(message.error);
          setIsStreaming(false);
          onError?.(message.error);
          return;
        }
        
        // It's a time series point
        const point: TimeSeriesPoint = {
          time_hour: message.time_hour,
          energy_generated_gw: message.energy_generated_gw,
          energy_received_gw: message.energy_received_gw,
        };
        
        setLiveData((prev) => [...prev, point]);
      } catch (e) {
        console.error("Failed to parse WebSocket message:", e);
      }
    };

    ws.onerror = (event) => {
      console.error("WebSocket error:", event);
      setError("WebSocket connection failed");
      setIsStreaming(false);
      onError?.("WebSocket connection failed");
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
      setIsStreaming(false);
    };
  }, [onComplete, onError]);

  const stopStreaming = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    setIsStreaming(false);
  }, []);

  const clearData = useCallback(() => {
    setLiveData([]);
    setError(null);
  }, []);

  return {
    liveData,
    isStreaming,
    error,
    startStreaming,
    stopStreaming,
    clearData,
  };
}
