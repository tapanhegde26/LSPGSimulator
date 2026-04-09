import PlotlyComponent from "react-plotly.js";

const Plot = (PlotlyComponent as any).default || PlotlyComponent;

type Props = {
  data: {
    total_energy_generated_gw: number;
    energy_received_gw: number;
  } | null;
};

export default function EnergyGraph({ data }: Props) {
  if (!data) return null;

  return (
    <div className="mt-4">
      <h2 className="text-xl font-semibold text-blue-300 mb-4 text-center">
        📈 Energy Comparison
      </h2>

      <Plot
        data={[
          {
            x: ["Generated", "Received"],
            y: [
              data.total_energy_generated_gw,
              data.energy_received_gw,
            ],
            type: "bar",
            marker: {
              color: ["#22c55e", "#3b82f6"], // green + blue
              line: {
                width: 1,
                color: "#0f172a",
              },
            },
            hoverinfo: "y",
          },
        ]}
        layout={{
          paper_bgcolor: "transparent",
          plot_bgcolor: "transparent",

          font: {
            color: "#cbd5f5",
            family: "Inter, sans-serif",
          },

          margin: { t: 20, b: 40, l: 40, r: 20 },

          xaxis: {
            showgrid: false,
            zeroline: false,
            tickfont: { size: 12 },
          },

          yaxis: {
            showgrid: true,
            gridcolor: "rgba(255,255,255,0.05)",
            zeroline: false,
          },

          bargap: 0.4,

          showlegend: false,
        }}
        config={{
          displayModeBar: false, // removes toolbar
          responsive: true,
        }}
        style={{ width: "100%", height: "300px" }}
      />
    </div>
  );
}