import { motion } from "framer-motion";
import { generateInsights } from "../utils/insights";

export default function Insights({ data }: any) {
  if (!data) return null;

  const insights = generateInsights(data);

  return (
    <div className="mt-8">
      <h2 className="text-xl font-semibold text-blue-300 mb-4">
        🧠 System Insights
      </h2>

      <div className="bg-slate-900/80 p-5 rounded-xl border border-slate-800 shadow-lg">
        {insights.map((insight, index) => (
          <motion.p
            key={index}
            className="text-gray-300 mb-2"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.2 }}
          >
            {insight}
          </motion.p>
        ))}
      </div>
    </div>
  );
}
