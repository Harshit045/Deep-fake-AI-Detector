import { motion } from "framer-motion";

export default function Scanner({ result, scanning }) {
  let glow = "border-cyan-400";
  let glowShadow = "shadow-cyan-500/40";
  let textColor = "text-cyan-400";

  if (
    result?.final_verdict === "DEEPFAKE" ||
    result?.final_verdict === "AI_GENERATED"
  ) {
    glow = "border-red-500";
    glowShadow = "shadow-red-500/40";
    textColor = "text-red-400";
  } else if (result?.final_verdict === "REAL_CAMERA") {
    glow = "border-green-500";
    glowShadow = "shadow-green-500/40";
    textColor = "text-green-400";
  }

  return (
    <div className="flex items-center justify-center">
      <div className="relative w-80 h-80 flex items-center justify-center">
        
        {/* Outer rotating ring */}
        <motion.div
          animate={scanning ? { rotate: 360 } : { rotate: 0 }}
          transition={{
            repeat: scanning ? Infinity : 0,
            duration: 2,
            ease: "linear",
          }}
          className={`absolute w-80 h-80 rounded-full border-4 ${glow} ${glowShadow} shadow-2xl`}
        />

        {/* Inner rotating ring reverse */}
        <motion.div
          animate={scanning ? { rotate: -360 } : { rotate: 0 }}
          transition={{
            repeat: scanning ? Infinity : 0,
            duration: 4,
            ease: "linear",
          }}
          className="absolute w-64 h-64 rounded-full border border-slate-600"
        />

        {/* Scanning beam */}
        {scanning && (
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
            className="absolute w-72 h-72 rounded-full"
          >
            <div className="w-2 h-36 bg-cyan-400 opacity-60 mx-auto rounded-full blur-sm"></div>
          </motion.div>
        )}

        {/* Pulse effect */}
        <motion.div
          animate={scanning ? { scale: [1, 1.05, 1] } : { scale: 1 }}
          transition={{
            repeat: scanning ? Infinity : 0,
            duration: 1,
          }}
          className="absolute w-56 h-56 rounded-full bg-slate-950 border border-slate-700 flex items-center justify-center"
        >
          <div className="text-center">
            <p className="text-slate-400 text-sm">Quantum Scanner</p>

            <motion.p
              animate={scanning ? { opacity: [1, 0.3, 1] } : { opacity: 1 }}
              transition={{ repeat: scanning ? Infinity : 0, duration: 0.3 }}
              className={`text-lg font-bold ${textColor}`}
            >
              {scanning ? "SCANNING..." : result?.final_verdict || "IDLE"}
            </motion.p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
