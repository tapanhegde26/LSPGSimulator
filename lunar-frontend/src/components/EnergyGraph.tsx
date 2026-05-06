/**
 * Energy Graph Component
 * Real-time visualization of energy generation and reception
 */
import PlotlyComponent from "react-plotly.js";
import type { TimeSeriesPoint } from "../types";
import { GraphSkeleton } from "./LoadingSpinner";

const Plot = (PlotlyComponent as { default?: typeof PlotlyComponent }).default || PlotlyComponent;

interface EnergyGraphProps {
  liveData: TimeSeriesPoint[];
  isLoading?: boolean;
}

export default function EnergyGraph({ liveData, isLoading = false }: EnergyGraphProps) {
  if (isLoading) {
    return <GraphSkeleton />;
  }

  if (!liveData || liveData.length === 0) {
    return (
      <div className="bg-slate-900/50 rounded-xl p-6 text-center">
        <p className="text-gray-500">
          Run a simulation to see real-time energy data
        </p>
      </div>
    );
  }

  const time = liveData.map((d) => d.time_hour);
  const generated = liveData.map((d) => d.energy_generated_gw);
  const received = liveData.map((d) => d.energy_received_gw);

  return (
    <div>
      <h2 className="text-xl font-semibold text-blue-300 mb-4">
        Live Energy Simulation
      </h2>

      <Plot
        data={[
          {
            x: time,
            y: generated,
            type: "scatter",
            mode: "lines+markers",
            name: "Generated",
            line: {
              color: "#22c55e",
              width: 3,
              shape: "spline",
            },
            marker: {
              size: 4,
            },
            fill: "tozeroy",
            fillcolor: "rgba(34,197,94,0.1)",
          },
          {
            x: time,
            y: received,
            type: "scatter",
            mode: "lines+markers",
            name: "Received",
            line: {
              color: "#3b82f6",
              width: 3,
              shape: "spline",
            },
            marker: {
              size: 4,
            },
            fill: "tozeroy",
            fillcolor: "rgba(59,130,246,0.1)",
          },
        ]}
        layout={{
          title: {
            text: "Real-Time Energy Flow",
            font: { color: "#e5e7eb", size: 16 },
          },
          paper_bgcolor: "transparent",
          plot_bgcolor: "transparent",
          font: { color: "#e5e7eb" },
          xaxis: {
            title: { text: "Time (hours)", font: { size: 12 } },
            gridcolor: "#1f2937",
            zerolinecolor: "#374151",
          },
          yaxis: {
            title: { text: "Energy (GW)", font: { size: 12 } },
            gridcolor: "#1f2937",
            zerolinecolor: "#374151",
          },
          legend: {
            orientation: "h",
            y: -0.2,
            x: 0.5,
            xanchor: "center",
          },
          margin: { t: 50, l: 60, r: 20, b: 60 },
          hovermode: "x unified",
        }}
        config={{ 
          displayModeBar: false,
          responsive: true,
        }}
        style={{ width: "100%", height: "300px" }}
      />

      {/* Stats summary */}
      <div className="grid grid-cols-3 gap-2 mt-4 text-center text-sm">
        <div className="bg-slate-800/50 p-2 rounded">
          <p className="text-gray-400">Data Points</p>
          <p className="text-white font-semibold">{liveData.length}</p>
        </div>
        <div className="bg-slate-800/50 p-2 rounded">
          <p className="text-gray-400">Avg Generated</p>
          <p className="text-green-400 font-semibold">
            {(generated.reduce((a, b) => a + b, 0) / generated.length).toFixed(1)} GW
          </p>
        </div>
        <div className="bg-slate-800/50 p-2 rounded">
          <p className="text-gray-400">Avg Received</p>
          <p className="text-blue-400 font-semibold">
            {(received.reduce((a, b) => a + b, 0) / received.length).toFixed(1)} GW
          </p>
        </div>
      </div>
    </div>
  );
}