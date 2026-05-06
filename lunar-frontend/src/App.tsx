/**
 * Lunar Solar Simulator - Main Application
 */
import SimulationForm from "./components/SimulationForm";
import Results from "./components/Results";
import EnergyGraph from "./components/EnergyGraph";
import Insights from "./components/Insights";
import MoonBackground from "./components/MoonBackground";
import EarthMoonSystem from "./components/EarthMoonSystem";
import { ErrorBoundary } from "./components/ErrorBoundary";
import { useSimulation } from "./hooks";
import type { SimulationInput } from "./types";

function App() {
  const {
    result,
    liveData,
    isLoading,
    isStreaming,
    error,
    runSimulationWithStreaming,
  } = useSimulation();

  const handleRun = async (input: SimulationInput) => {
    await runSimulationWithStreaming(input);
  };

  return (
    <div className="relative min-h-screen bg-black text-white overflow-hidden p-6">
      {/* Background */}
      <div className="absolute inset-0 -z-20 opacity-20">
        <ErrorBoundary fallback={<div className="w-full h-full bg-slate-900" />}>
          <MoonBackground />
        </ErrorBoundary>
      </div>

      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-black via-slate-900 to-black" />

      {/* Radial glow effect */}
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_center,rgba(59,130,246,0.08),transparent_70%)] pointer-events-none" />

      {/* Header */}
      <header className="text-center mb-8 relative z-10">
        <h1 className="text-4xl md:text-5xl font-bold text-blue-400 drop-shadow-[0_0_25px_rgba(59,130,246,0.9)]">
          Lunar Solar Ring Simulator
        </h1>
        <p className="text-gray-400 mt-2 max-w-2xl mx-auto">
          Interactive simulation of space-based solar power generation from the Moon
          and wireless energy transmission to Earth
        </p>
        
        {/* Status indicator */}
        <div className="mt-4 flex items-center justify-center gap-2 text-sm">
          <span
            className={`w-2 h-2 rounded-full ${
              isStreaming ? "bg-green-400 animate-pulse" : "bg-gray-500"
            }`}
          />
          <span className="text-gray-500">
            {isStreaming ? "Streaming live data..." : "Ready"}
          </span>
        </div>
      </header>

      {/* Error Alert */}
      {error && (
        <div className="max-w-4xl mx-auto mb-6 bg-red-900/50 border border-red-500 rounded-lg p-4 text-center">
          <p className="text-red-300">{error}</p>
        </div>
      )}

      {/* Main Content */}
      <div className="max-w-7xl mx-auto relative z-10">
        {/* 3D Visualization - Full Width */}
        <div className="mb-6 bg-slate-900/90 backdrop-blur-sm rounded-2xl border border-slate-800 shadow-lg overflow-hidden">
          <div className="p-4 border-b border-slate-800">
            <h2 className="text-lg font-semibold text-blue-300">
              Earth-Moon Energy System
            </h2>
            <p className="text-xs text-gray-500 mt-1">
              3D visualization of the lunar solar ring and energy transmission
            </p>
          </div>
          <ErrorBoundary fallback={
            <div className="h-[400px] flex items-center justify-center text-gray-500">
              3D visualization unavailable
            </div>
          }>
            <EarthMoonSystem 
              simulationData={result} 
              isStreaming={isStreaming}
            />
          </ErrorBoundary>
        </div>

        {/* Two Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Panel - Controls */}
          <div className="bg-slate-900/90 backdrop-blur-sm p-6 rounded-2xl border border-slate-800 shadow-lg">
            <SimulationForm
              onRun={handleRun}
              isLoading={isLoading}
              isStreaming={isStreaming}
            />
          </div>

          {/* Right Panel - Graph */}
          <div className="bg-slate-900/90 backdrop-blur-sm p-6 rounded-2xl border border-slate-800 shadow-lg">
            <ErrorBoundary>
              <EnergyGraph liveData={liveData} isLoading={isLoading} />
            </ErrorBoundary>
          </div>
        </div>

        {/* Results Section */}
        <div className="mt-6">
          <ErrorBoundary>
            <Results data={result} isLoading={isLoading} />
          </ErrorBoundary>
        </div>

        {/* Insights Section */}
        <div>
          <ErrorBoundary>
            <Insights data={result} />
          </ErrorBoundary>
        </div>
      </div>

      {/* Footer */}
      <footer className="mt-16 text-center text-gray-600 text-sm relative z-10">
        <p>
          Lunar Solar Ring Simulator v2.0 | Inspired by space-based solar power concepts
        </p>
        <p className="mt-1 text-xs text-gray-700">
          Built with React, Three.js, FastAPI, and Python
        </p>
      </footer>
    </div>
  );
}

export default App;