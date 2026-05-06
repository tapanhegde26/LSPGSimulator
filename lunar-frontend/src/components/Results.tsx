/**
 * Results Component
 * Displays simulation results in animated cards
 */
import { motion } from "framer-motion";
import type { SimulationResponse } from "../types";
import { CardSkeleton } from "./LoadingSpinner";

interface ResultsProps {
  data: SimulationResponse | null;
  isLoading?: boolean;
}

export default function Results({ data, isLoading = false }: ResultsProps) {
  if (isLoading) {
    return (
      <div className="mt-8">
        <h2 className="text-2xl font-semibold text-blue-300 mb-4">
          Simulation Results
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => (
            <CardSkeleton key={i} />
          ))}
        </div>
      </div>
    );
  }

  if (!data) return null;

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

  const formatNumber = (num: number, decimals: number = 2): string => {
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`;
    }
    if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K`;
    }
    return num.toFixed(decimals);
  };

  return (
    <div className="mt-8">
      <h2 className="text-2xl font-semibold text-blue-300 mb-4">
        Simulation Results
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
          className="bg-slate-900 p-5 rounded-xl shadow-lg text-center border border-slate-800 hover:shadow-green-500/20 hover:scale-105 transition duration-300"
        >
          <p className="text-gray-400 text-sm">Generated Energy</p>
          <h3 className="text-2xl font-bold text-green-400 mt-2">
            {formatNumber(data.total_energy_generated_gw)} GW
          </h3>
          <p className="text-xs text-gray-500 mt-1">Total lunar ring output</p>
        </motion.div>

        {/* Received Energy */}
        <motion.div
          variants={card}
          transition={{ duration: 0.4 }}
          className="bg-slate-900 p-5 rounded-xl shadow-lg text-center border border-slate-800 hover:shadow-blue-500/20 hover:scale-105 transition duration-300"
        >
          <p className="text-gray-400 text-sm">Received on Earth</p>
          <h3 className="text-2xl font-bold text-blue-400 mt-2">
            {formatNumber(data.energy_received_gw)} GW
          </h3>
          <p className="text-xs text-gray-500 mt-1">After transmission</p>
        </motion.div>

        {/* Transmission Loss */}
        <motion.div
          variants={card}
          transition={{ duration: 0.4 }}
          className="bg-slate-900 p-5 rounded-xl shadow-lg text-center border border-slate-800 hover:shadow-red-500/20 hover:scale-105 transition duration-300"
        >
          <p className="text-gray-400 text-sm">Transmission Loss</p>
          <h3 className="text-2xl font-bold text-red-400 mt-2">
            {data.transmission_loss_percent.toFixed(1)}%
          </h3>
          <p className="text-xs text-gray-500 mt-1">Energy lost in transit</p>
        </motion.div>

        {/* System Efficiency */}
        <motion.div
          variants={card}
          transition={{ duration: 0.4 }}
          className="bg-slate-900 p-5 rounded-xl shadow-lg text-center border border-slate-800 hover:shadow-purple-500/20 hover:scale-105 transition duration-300"
        >
          <p className="text-gray-400 text-sm">System Efficiency</p>
          <h3 className="text-2xl font-bold text-purple-400 mt-2">
            {(data.system_efficiency * 100).toFixed(1)}%
          </h3>
          <p className="text-xs text-gray-500 mt-1">Overall performance</p>
        </motion.div>
      </motion.div>

      {/* Ground Stations Distribution */}
      {data.stations && data.stations.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mt-6 bg-slate-900/50 p-4 rounded-xl border border-slate-800"
        >
          <h3 className="text-lg font-semibold text-gray-300 mb-3">
            Ground Station Distribution
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
            {data.stations.map((station) => (
              <div
                key={station.station_id}
                className="bg-slate-800 p-3 rounded-lg text-center"
              >
                <p className="text-xs text-gray-400">Station {station.station_id}</p>
                <p className="text-sm font-semibold text-cyan-400">
                  {formatNumber(station.received_gw)} GW
                </p>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}
