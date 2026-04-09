import { motion } from "framer-motion";

type SimulationResult = {
  total_energy_generated_gw: number;
  energy_received_gw: number;
  transmission_loss_percent: number;
  system_efficiency: number;
};

type Props = {
  data: SimulationResult | null;
};

export default function Results({ data }: Props) {
  if (!data) return null;

  // Animation variants
  const container = {
    hidden: {},
    visible: {
      transition: {
        staggerChildren: 0.15,
      },
    },
  };

  const card = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0 },
  };

  return (
    <div className="mt-8">
      <h2 className="text-2xl font-semibold text-blue-300 mb-4">
        📊 Simulation Results
      </h2>

      <motion.div
        className="grid grid-cols-1 md:grid-cols-4 gap-4"
        variants={container}
        initial="hidden"
        animate="visible"
      >
        
        {/* Generated Energy */}
        <motion.div
          variants={card}
          transition={{ duration: 0.4 }}
          className="bg-slate-900 p-5 rounded-xl shadow-lg text-center border border-slate-800 hover:shadow-blue-500/30 hover:scale-105 transition duration-300"
        >
          <p className="text-gray-400 text-sm">⚡ Generated Energy</p>
          <h3 className="text-2xl font-bold text-green-400 mt-2">
            {data.total_energy_generated_gw.toFixed(2)} GW
          </h3>
        </motion.div>

        {/* Received Energy */}
        <motion.div
          variants={card}
          transition={{ duration: 0.4 }}
          className="bg-slate-900 p-5 rounded-xl shadow-lg text-center border border-slate-800 hover:shadow-blue-500/30 hover:scale-105 transition duration-300"
        >
          <p className="text-gray-400 text-sm">📡 Received Energy</p>
          <h3 className="text-2xl font-bold text-blue-400 mt-2">
            {data.energy_received_gw.toFixed(2)} GW
          </h3>
        </motion.div>

        {/* Loss */}
        <motion.div
          variants={card}
          transition={{ duration: 0.4 }}
          className="bg-slate-900 p-5 rounded-xl shadow-lg text-center border border-slate-800 hover:shadow-blue-500/30 hover:scale-105 transition duration-300"
        >
          <p className="text-gray-400 text-sm">🔥 Transmission Loss</p>
          <h3 className="text-2xl font-bold text-red-400 mt-2">
            {data.transmission_loss_percent.toFixed(2)}%
          </h3>
        </motion.div>

        {/* Efficiency */}
        <motion.div
          variants={card}
          transition={{ duration: 0.4 }}
          className="bg-slate-900 p-5 rounded-xl shadow-lg text-center border border-slate-800 hover:shadow-blue-500/30 hover:scale-105 transition duration-300"
        >
          <p className="text-gray-400 text-sm">⚙️ System Efficiency</p>
          <h3 className="text-2xl font-bold text-purple-400 mt-2">
            {(data.system_efficiency * 100).toFixed(2)}%
          </h3>
        </motion.div>

      </motion.div>
    </div>
  );
}
