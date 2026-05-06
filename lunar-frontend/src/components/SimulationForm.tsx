/**
 * Simulation Form Component
 * Provides controls for configuring simulation parameters
 */
import { useState, FormEvent } from "react";
import * as Slider from "@radix-ui/react-slider";
import type { SimulationInput, TransmissionType } from "../types";
import { DEFAULT_SIMULATION_INPUT, VALIDATION_CONSTRAINTS } from "../types";

interface SimulationFormProps {
  onRun: (input: SimulationInput) => void;
  isLoading?: boolean;
  isStreaming?: boolean;
}

export default function SimulationForm({ 
  onRun, 
  isLoading = false,
  isStreaming = false 
}: SimulationFormProps) {
  const [form, setForm] = useState<SimulationInput>(DEFAULT_SIMULATION_INPUT);

  const updateField = <K extends keyof SimulationInput>(
    key: K, 
    value: SimulationInput[K]
  ) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log("Simulation request:", form);
    onRun(form);
  };

  const isDisabled = isLoading || isStreaming;

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <h2 className="text-xl font-semibold text-blue-300">
        Simulation Parameters
      </h2>

      {/* Ring Width */}
      <div>
        <label className="flex justify-between text-sm text-gray-300">
          <span>Ring Width (km)</span>
          <input
            type="number"
            value={form.ring_width_km}
            onChange={(e) =>
              updateField("ring_width_km", Number(e.target.value))
            }
            min={VALIDATION_CONSTRAINTS.ring_width_km.min}
            max={VALIDATION_CONSTRAINTS.ring_width_km.max}
            className="w-20 bg-slate-800 rounded px-2 text-sm text-white"
            disabled={isDisabled}
          />
        </label>

        <Slider.Root
          min={VALIDATION_CONSTRAINTS.ring_width_km.min}
          max={VALIDATION_CONSTRAINTS.ring_width_km.max}
          step={1}
          value={[form.ring_width_km]}
          onValueChange={(val) => updateField("ring_width_km", val[0])}
          className="mt-2 relative flex items-center select-none touch-none w-full h-5"
          disabled={isDisabled}
        >
          <Slider.Track className="bg-slate-700 relative grow rounded-full h-2">
            <Slider.Range className="absolute bg-blue-500 rounded-full h-full" />
          </Slider.Track>
          <Slider.Thumb 
            className="block w-4 h-4 bg-white rounded-full shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            aria-label="Ring Width"
          />
        </Slider.Root>
        <p className="text-xs text-gray-500 mt-1">
          Width of solar panel ring around Moon's equator
        </p>
      </div>

      {/* Panel Efficiency */}
      <div>
        <label className="flex justify-between text-sm text-gray-300">
          <span>Panel Efficiency (%)</span>
          <span className="text-green-400 font-mono">
            {(form.panel_efficiency * 100).toFixed(0)}%
          </span>
        </label>

        <Slider.Root
          min={VALIDATION_CONSTRAINTS.panel_efficiency.min}
          max={VALIDATION_CONSTRAINTS.panel_efficiency.max}
          step={0.01}
          value={[form.panel_efficiency]}
          onValueChange={(val) => updateField("panel_efficiency", val[0])}
          className="mt-2 relative flex items-center select-none touch-none w-full h-5"
          disabled={isDisabled}
        >
          <Slider.Track className="bg-slate-700 relative grow rounded-full h-2">
            <Slider.Range className="absolute bg-green-500 rounded-full h-full" />
          </Slider.Track>
          <Slider.Thumb 
            className="block w-4 h-4 bg-white rounded-full shadow-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            aria-label="Panel Efficiency"
          />
        </Slider.Root>
        <p className="text-xs text-gray-500 mt-1">
          Solar panel conversion efficiency (current tech: 20-25%)
        </p>
      </div>

      {/* Transmission Type */}
      <div>
        <label className="text-sm text-gray-300">Transmission Type</label>
        <select
          className="w-full mt-1 p-2 bg-slate-800 rounded text-white border border-slate-700 focus:border-blue-500 focus:outline-none"
          value={form.transmission_type}
          onChange={(e) =>
            updateField("transmission_type", e.target.value as TransmissionType)
          }
          disabled={isDisabled}
        >
          <option value="microwave">Microwave (Lower loss, proven tech)</option>
          <option value="laser">Laser (Higher loss, more focused)</option>
        </select>
      </div>

      {/* Ground Stations */}
      <div>
        <label className="flex justify-between text-sm text-gray-300">
          <span>Ground Stations</span>
          <span className="text-purple-400 font-mono">{form.num_ground_stations}</span>
        </label>

        <Slider.Root
          min={VALIDATION_CONSTRAINTS.num_ground_stations.min}
          max={VALIDATION_CONSTRAINTS.num_ground_stations.max}
          step={1}
          value={[form.num_ground_stations]}
          onValueChange={(val) => updateField("num_ground_stations", val[0])}
          className="mt-2 relative flex items-center select-none touch-none w-full h-5"
          disabled={isDisabled}
        >
          <Slider.Track className="bg-slate-700 relative grow rounded-full h-2">
            <Slider.Range className="absolute bg-purple-500 rounded-full h-full" />
          </Slider.Track>
          <Slider.Thumb 
            className="block w-4 h-4 bg-white rounded-full shadow-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            aria-label="Ground Stations"
          />
        </Slider.Root>
        <p className="text-xs text-gray-500 mt-1">
          Number of Earth receiving stations (rectennas)
        </p>
      </div>

      {/* Simulation Duration */}
      <div>
        <label className="flex justify-between text-sm text-gray-300">
          <span>Simulation Duration</span>
          <span className="text-yellow-400 font-mono">{form.simulation_hours}h</span>
        </label>

        <Slider.Root
          min={VALIDATION_CONSTRAINTS.simulation_hours.min}
          max={VALIDATION_CONSTRAINTS.simulation_hours.max}
          step={1}
          value={[form.simulation_hours]}
          onValueChange={(val) => updateField("simulation_hours", val[0])}
          className="mt-2 relative flex items-center select-none touch-none w-full h-5"
          disabled={isDisabled}
        >
          <Slider.Track className="bg-slate-700 relative grow rounded-full h-2">
            <Slider.Range className="absolute bg-yellow-500 rounded-full h-full" />
          </Slider.Track>
          <Slider.Thumb 
            className="block w-4 h-4 bg-white rounded-full shadow-lg focus:outline-none focus:ring-2 focus:ring-yellow-500"
            aria-label="Simulation Hours"
          />
        </Slider.Root>
        <p className="text-xs text-gray-500 mt-1">
          Duration in hours (max 168h = 1 week)
        </p>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isDisabled}
        className={`w-full p-3 rounded-lg font-semibold transition-all duration-300 ${
          isDisabled
            ? "bg-slate-700 text-slate-400 cursor-not-allowed"
            : "bg-blue-500 hover:bg-blue-600 text-white shadow-lg hover:shadow-blue-500/30 hover:scale-[1.02]"
        }`}
      >
        {isLoading ? (
          <span className="flex items-center justify-center gap-2">
            <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            Running Simulation...
          </span>
        ) : isStreaming ? (
          <span className="flex items-center justify-center gap-2">
            <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
            Streaming Data...
          </span>
        ) : (
          "Run Simulation"
        )}
      </button>
    </form>
  );
}