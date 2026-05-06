import { motion } from "framer-motion";

export default function EnergyBeam() {
  return (
    <div className="absolute w-full h-full flex items-center justify-center pointer-events-none">

      {/* Main Beam */}
      <motion.div
        className="absolute h-2 w-[70%] bg-gradient-to-r from-blue-400 via-cyan-300 to-blue-400 rounded-full blur-sm rotate-6 -translate-y-4"
        initial={{ opacity: 0.3, scaleX: 0.8 }}
        animate={{
          opacity: [0.3, 1, 0.3],
          scaleX: [0.8, 1.1, 0.8],
        }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
        }}
      />

      {/* Glow Layer */}
      <motion.div
        className="absolute h-4 w-[70%] bg-blue-400/20 rounded-full blur-xl"
        animate={{
          opacity: [0.2, 0.6, 0.2],
        }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
        }}
      />

      {/* Moving Energy Pulse */}
      <motion.div
        className="absolute h-3 w-20 bg-white rounded-full blur-md"
        initial={{ x: "-40%" }}
        animate={{ x: "40%" }}
        transition={{
          duration: 1,
          repeat: Infinity,
          ease: "linear",
        }}
      />
    </div>
  );
}