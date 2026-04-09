import { useState } from "react";
import SimulationForm from "./components/SimulationForm";
import Results from "./components/Results";
import EnergyGraph from "./components/EnergyGraph";
import Insights from "./components/Insights";
import MoonVisual from "./components/MoonVisual";
import MoonBackground from "./components/MoonBackground";
import EnergyBeam from "./components/EnergyBeam";
import { runSimulation } from "./services/api";

function App() {
  const [result, setResult] = useState(null);

  const handleRun = async (input: any) => {
    try {
      const data = await runSimulation(input);
      setResult(data);
    } catch (err) {
      alert("Simulation failed");
      console.error(err);
    }
  };

  return (
    <div className="relative min-h-screen bg-black text-white overflow-hidden p-6">

      {/* 🌕 Moon Background (deep layer) */}
      <div className="absolute inset-0 -z-20 opacity-30">
        <MoonBackground />
      </div>

      {/* 🌌 Base Gradient Background */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-black via-slate-900 to-black"></div>

      {/* ✨ Center Glow Overlay */}
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_center,rgba(59,130,246,0.12),transparent_70%)] pointer-events-none"></div>

      {/* 🌠 Top Accent Glow */}
      <div className="absolute top-0 left-0 w-full h-64 bg-gradient-to-b from-blue-500/10 to-transparent blur-2xl -z-10"></div>

      {/* 🌠 Bottom Accent Glow */}
      <div className="absolute bottom-0 left-0 w-full h-64 bg-gradient-to-t from-purple-500/10 to-transparent blur-2xl -z-10"></div>

      {/* Header */}
      <div className="text-center mb-10 relative z-10">
        <h1 className="text-4xl md:text-5xl font-bold text-blue-400 drop-shadow-[0_0_25px_rgba(59,130,246,0.9)]">
          🌕 Lunar Solar Simulator
        </h1>
        <p className="text-gray-400 mt-3 text-lg">
          Simulating Space-Based Solar Energy Transmission
        </p>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 relative z-10">
        
        {/* Left Panel */}
        <div className="bg-slate-900/90 backdrop-blur-sm p-6 rounded-2xl shadow-lg border border-slate-800 hover:shadow-blue-500/20 transition duration-300">
          <SimulationForm onRun={handleRun} />
        </div>

        {/* Right Panel */}
        <div className="bg-slate-900/90 backdrop-blur-sm p-6 rounded-2xl shadow-lg border border-slate-800 hover:shadow-purple-500/20 transition duration-300">
          
          {/* 🌕 Moon + Energy Beam */}
          <div className="relative flex justify-center items-center">
            <MoonVisual />
            <EnergyBeam />
          </div>

          {/* 📈 Graph */}
          <div className="mt-4">
            <EnergyGraph data={result} />
          </div>
        </div>
      </div>

      {/* Results */}
      <div className="mt-10 relative z-10">
        <Results data={result} />
      </div>

      {/* 🧠 Insights */}
      <div className="relative z-10">
        <Insights data={result} />
      </div>
    </div>
  );
}

export default App;
