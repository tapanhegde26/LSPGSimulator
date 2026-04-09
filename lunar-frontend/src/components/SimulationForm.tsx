import { useState } from "react";
import * as Slider from "@radix-ui/react-slider";

export default function SimulationForm({ onRun }: any) {
  const [form, setForm] = useState({
    ring_width_km: 50,
    panel_efficiency: 0.22,
    transmission_type: "microwave",
    num_ground_stations: 5,
  });

  const handleSubmit = (e: any) => {
    e.preventDefault();
    onRun(form);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <h2 className="text-xl font-semibold text-blue-300">⚙️ Simulation Input</h2>

      {/* Ring Width */}
      <div>
        <label>Ring Width: {form.ring_width_km} km</label>
        <Slider.Root
          className="relative flex items-center w-full h-5 mt-2"
          min={1}
          max={400}
          step={1}
          value={[form.ring_width_km]}
          onValueChange={(val) =>
            setForm({ ...form, ring_width_km: val[0] })
          }
        >
          <Slider.Track className="bg-slate-700 relative grow rounded-full h-2">
            <Slider.Range className="absolute bg-blue-500 h-full rounded-full" />
          </Slider.Track>
          <Slider.Thumb className="block w-4 h-4 bg-white rounded-full" />
        </Slider.Root>
      </div>

      {/* Efficiency */}
      <div>
        <label>Efficiency: {form.panel_efficiency}</label>
        <Slider.Root
          min={0.1}
          max={0.5}
          step={0.01}
          value={[form.panel_efficiency]}
          onValueChange={(val) =>
            setForm({ ...form, panel_efficiency: val[0] })
          }
        >
          <Slider.Track className="bg-slate-700 h-2 rounded">
            <Slider.Range className="bg-green-500 h-full rounded" />
          </Slider.Track>
          <Slider.Thumb className="w-4 h-4 bg-white rounded-full" />
        </Slider.Root>
      </div>

      {/* Transmission */}
      <div>
        <label>Transmission</label>
        <select
          className="w-full mt-1 p-2 bg-slate-800 rounded"
          value={form.transmission_type}
          onChange={(e) =>
            setForm({ ...form, transmission_type: e.target.value })
          }
        >
          <option value="microwave">Microwave</option>
          <option value="laser">Laser</option>
        </select>
      </div>

      {/* Stations */}
      <div>
        <label>Ground Stations: {form.num_ground_stations}</label>
        <Slider.Root
          min={1}
          max={20}
          step={1}
          value={[form.num_ground_stations]}
          onValueChange={(val) =>
            setForm({ ...form, num_ground_stations: val[0] })
          }
        >
          <Slider.Track className="bg-slate-700 h-2 rounded">
            <Slider.Range className="bg-purple-500 h-full rounded" />
          </Slider.Track>
          <Slider.Thumb className="w-4 h-4 bg-white rounded-full" />
        </Slider.Root>
      </div>

      <button className="w-full bg-blue-500 hover:bg-blue-600 p-2 rounded font-semibold transition">
        Run Simulation 🚀
      </button>
    </form>
  );
}
