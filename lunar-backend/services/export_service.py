"""
Data Export Service
Exports simulation results in various formats (JSON, CSV, PDF).
"""
import json
import csv
import io
from typing import Dict, List, Literal, Optional
from datetime import datetime

from models.response import SimulationResponse


def export_to_json(
    simulation_result: SimulationResponse,
    include_time_series: bool = True,
    pretty_print: bool = True,
) -> str:
    """
    Export simulation results to JSON format.
    
    Args:
        simulation_result: Simulation response object
        include_time_series: Include detailed time series data
        pretty_print: Format JSON with indentation
        
    Returns:
        JSON string
    """
    data = {
        "export_timestamp": datetime.utcnow().isoformat(),
        "simulation_results": {
            "total_energy_generated_gw": simulation_result.total_energy_generated_gw,
            "energy_received_gw": simulation_result.energy_received_gw,
            "transmission_loss_percent": simulation_result.transmission_loss_percent,
            "system_efficiency": simulation_result.system_efficiency,
            "insights": simulation_result.insights,
        },
        "ground_stations": [
            {
                "station_id": s.station_id,
                "received_gw": s.received_gw,
                "latitude": s.latitude,
                "longitude": s.longitude,
                "name": s.name,
            }
            for s in simulation_result.stations
        ],
    }
    
    if include_time_series:
        data["time_series"] = [
            {
                "time_hour": p.time_hour,
                "energy_generated_gw": p.energy_generated_gw,
                "energy_received_gw": p.energy_received_gw,
            }
            for p in simulation_result.time_series
        ]
    
    if simulation_result.optimization:
        data["optimization"] = {
            "optimal_ring_width_km": simulation_result.optimization.optimal_ring_width_km,
            "optimal_efficiency": simulation_result.optimization.optimal_efficiency,
            "optimal_stations": simulation_result.optimization.optimal_stations,
            "optimal_transmission_type": simulation_result.optimization.optimal_transmission_type,
            "predicted_energy_gw": simulation_result.optimization.predicted_energy_gw,
            "improvement_percent": simulation_result.optimization.improvement_percent,
        }
    
    indent = 2 if pretty_print else None
    return json.dumps(data, indent=indent)


def export_to_csv(
    simulation_result: SimulationResponse,
    data_type: Literal["summary", "time_series", "stations"] = "time_series",
) -> str:
    """
    Export simulation results to CSV format.
    
    Args:
        simulation_result: Simulation response object
        data_type: Type of data to export
        
    Returns:
        CSV string
    """
    output = io.StringIO()
    
    if data_type == "summary":
        writer = csv.writer(output)
        writer.writerow(["Metric", "Value", "Unit"])
        writer.writerow(["Total Energy Generated", simulation_result.total_energy_generated_gw, "GW"])
        writer.writerow(["Energy Received", simulation_result.energy_received_gw, "GW"])
        writer.writerow(["Transmission Loss", simulation_result.transmission_loss_percent, "%"])
        writer.writerow(["System Efficiency", simulation_result.system_efficiency * 100, "%"])
        writer.writerow(["Number of Stations", len(simulation_result.stations), ""])
        writer.writerow(["Simulation Hours", len(simulation_result.time_series), "hours"])
        
    elif data_type == "time_series":
        writer = csv.writer(output)
        writer.writerow(["Hour", "Energy Generated (GW)", "Energy Received (GW)", "Loss (GW)"])
        for point in simulation_result.time_series:
            loss = point.energy_generated_gw - point.energy_received_gw
            writer.writerow([
                point.time_hour,
                round(point.energy_generated_gw, 2),
                round(point.energy_received_gw, 2),
                round(loss, 2),
            ])
            
    elif data_type == "stations":
        writer = csv.writer(output)
        writer.writerow(["Station ID", "Name", "Latitude", "Longitude", "Received Energy (GW)"])
        for station in simulation_result.stations:
            writer.writerow([
                station.station_id,
                station.name or f"Station {station.station_id}",
                station.latitude or "N/A",
                station.longitude or "N/A",
                round(station.received_gw, 2),
            ])
    
    return output.getvalue()


def generate_report_html(
    simulation_result: SimulationResponse,
    input_params: Optional[Dict] = None,
) -> str:
    """
    Generate an HTML report for the simulation.
    
    Args:
        simulation_result: Simulation response object
        input_params: Original input parameters
        
    Returns:
        HTML string
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Generate time series chart data
    time_labels = [str(p.time_hour) for p in simulation_result.time_series[:48]]
    generated_data = [round(p.energy_generated_gw, 2) for p in simulation_result.time_series[:48]]
    received_data = [round(p.energy_received_gw, 2) for p in simulation_result.time_series[:48]]
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lunar Solar Simulation Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            padding: 2rem;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #60a5fa; margin-bottom: 0.5rem; }}
        h2 {{ color: #94a3b8; font-size: 1.25rem; margin: 2rem 0 1rem; }}
        .timestamp {{ color: #64748b; font-size: 0.875rem; margin-bottom: 2rem; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }}
        .card {{
            background: #1e293b;
            border-radius: 0.75rem;
            padding: 1.5rem;
            border: 1px solid #334155;
        }}
        .card-label {{ color: #94a3b8; font-size: 0.875rem; }}
        .card-value {{ font-size: 1.5rem; font-weight: bold; margin-top: 0.5rem; }}
        .green {{ color: #4ade80; }}
        .blue {{ color: #60a5fa; }}
        .red {{ color: #f87171; }}
        .purple {{ color: #a78bfa; }}
        .chart-container {{ background: #1e293b; border-radius: 0.75rem; padding: 1.5rem; margin-top: 1rem; }}
        .insights {{ margin-top: 2rem; }}
        .insight {{ 
            background: #1e293b; 
            padding: 1rem; 
            border-radius: 0.5rem; 
            margin-bottom: 0.5rem;
            border-left: 4px solid #eab308;
        }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
        th, td {{ padding: 0.75rem; text-align: left; border-bottom: 1px solid #334155; }}
        th {{ color: #94a3b8; font-weight: 500; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Lunar Solar Ring Simulation Report</h1>
        <p class="timestamp">Generated: {timestamp}</p>
        
        <h2>Summary Results</h2>
        <div class="grid">
            <div class="card">
                <div class="card-label">Energy Generated</div>
                <div class="card-value green">{simulation_result.total_energy_generated_gw:,.2f} GW</div>
            </div>
            <div class="card">
                <div class="card-label">Energy Received</div>
                <div class="card-value blue">{simulation_result.energy_received_gw:,.2f} GW</div>
            </div>
            <div class="card">
                <div class="card-label">Transmission Loss</div>
                <div class="card-value red">{simulation_result.transmission_loss_percent:.1f}%</div>
            </div>
            <div class="card">
                <div class="card-label">System Efficiency</div>
                <div class="card-value purple">{simulation_result.system_efficiency * 100:.1f}%</div>
            </div>
        </div>
        
        <h2>Energy Over Time</h2>
        <div class="chart-container">
            <canvas id="energyChart"></canvas>
        </div>
        
        <h2>Ground Stations ({len(simulation_result.stations)})</h2>
        <table>
            <thead>
                <tr>
                    <th>Station</th>
                    <th>Location</th>
                    <th>Energy Received</th>
                </tr>
            </thead>
            <tbody>
                {"".join(f'''
                <tr>
                    <td>Station {s.station_id}</td>
                    <td>{s.name or 'N/A'}</td>
                    <td>{s.received_gw:.2f} GW</td>
                </tr>
                ''' for s in simulation_result.stations)}
            </tbody>
        </table>
        
        <div class="insights">
            <h2>Insights</h2>
            {"".join(f'<div class="insight">{insight}</div>' for insight in simulation_result.insights)}
        </div>
    </div>
    
    <script>
        const ctx = document.getElementById('energyChart').getContext('2d');
        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: {time_labels},
                datasets: [
                    {{
                        label: 'Generated (GW)',
                        data: {generated_data},
                        borderColor: '#4ade80',
                        backgroundColor: 'rgba(74, 222, 128, 0.1)',
                        fill: true,
                        tension: 0.4,
                    }},
                    {{
                        label: 'Received (GW)',
                        data: {received_data},
                        borderColor: '#60a5fa',
                        backgroundColor: 'rgba(96, 165, 250, 0.1)',
                        fill: true,
                        tension: 0.4,
                    }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ labels: {{ color: '#94a3b8' }} }}
                }},
                scales: {{
                    x: {{ 
                        title: {{ display: true, text: 'Hour', color: '#94a3b8' }},
                        ticks: {{ color: '#64748b' }},
                        grid: {{ color: '#334155' }}
                    }},
                    y: {{ 
                        title: {{ display: true, text: 'Energy (GW)', color: '#94a3b8' }},
                        ticks: {{ color: '#64748b' }},
                        grid: {{ color: '#334155' }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    return html
