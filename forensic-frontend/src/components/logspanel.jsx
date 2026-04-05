import { useEffect, useState } from "react";

export default function LogsPanel({ scanning, result }) {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    if (scanning) {
      setLogs([
        "[SYSTEM] Initializing forensic engine...",
        "[SCAN] Reading image pixels...",
        "[AI] Extracting facial landmarks...",
        "[MODEL] Running CNN classification...",
        "[META] Checking EXIF metadata...",
        "[FORENSICS] Detecting AI artifacts...",
      ]);
    }
  }, [scanning]);

  useEffect(() => {
    if (result) {
      setLogs((prev) => [
        ...prev,
        `[RESULT] Verdict Generated: ${result.final_verdict}`,
        `[RISK] Deepfake Score: ${result.deepfake_score}`,
        `[RISK] AI Artifact Score: ${result.ai_score}`,
        "[SYSTEM] Analysis Completed Successfully ✅",
      ]);
    }
  }, [result]);

  return (
    <div className="bg-black/60 border border-cyan-500/40 rounded-xl p-4 h-56 overflow-y-auto shadow-lg">
      <h2 className="text-cyan-400 font-bold mb-2">Live Scan Logs</h2>

      <div className="text-green-400 font-mono text-sm space-y-1">
        {logs.length === 0 ? (
          <p className="text-slate-400">Waiting for scan...</p>
        ) : (
          logs.map((log, i) => <p key={i}>{log}</p>)
        )}
      </div>
    </div>
  );
}
