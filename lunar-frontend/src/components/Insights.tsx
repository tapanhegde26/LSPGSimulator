/**
 * Insights Component
 * Displays AI-generated insights and recommendations
 */
import { motion } from "framer-motion";
import type { SimulationResponse } from "../types";

interface InsightsProps {
  data: SimulationResponse | null;
}

export default function Insights({ data }: InsightsProps) {
  if (!data?.insights || data.insights.length === 0) return null;

  const container = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const item = {
    hidden: { opacity: 0, x: -20 },
    visible: { opacity: 1, x: 0 },
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
      className="mt-8 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-lg"
    >
      <h2 className="text-xl font-semibold text-yellow-300 mb-4">
        Smart Insights
      </h2>

      <motion.ul
        className="space-y-2"
        variants={container}
        initial="hidden"
        animate="visible"
      >
        {data.insights.map((insight, idx) => (
          <motion.li
            key={idx}
            variants={item}
            className="text-gray-300 bg-slate-800/80 p-3 rounded-lg border-l-4 border-yellow-500/50 hover:border-yellow-500 transition-colors"
          >
            {insight}
          </motion.li>
        ))}
      </motion.ul>

      {/* Efficiency indicator */}
      <div className="mt-4 pt-4 border-t border-slate-700">
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-400">Overall Assessment</span>
          <span
            className={`font-semibold ${
              data.system_efficiency > 0.8
                ? "text-green-400"
                : data.system_efficiency > 0.6
                ? "text-yellow-400"
                : "text-red-400"
            }`}
          >
            {data.system_efficiency > 0.8
              ? "Excellent Configuration"
              : data.system_efficiency > 0.6
              ? "Good Configuration"
              : "Needs Optimization"}
          </span>
        </div>
        <div className="mt-2 h-2 bg-slate-700 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${data.system_efficiency * 100}%` }}
            transition={{ duration: 1, ease: "easeOut" }}
            className={`h-full rounded-full ${
              data.system_efficiency > 0.8
                ? "bg-green-500"
                : data.system_efficiency > 0.6
                ? "bg-yellow-500"
                : "bg-red-500"
            }`}
          />
        </div>
      </div>
    </motion.div>
  );
}