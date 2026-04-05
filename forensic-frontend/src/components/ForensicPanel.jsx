export default function ForensicPanel({ result }) {
  if (!result) {
    return (
      <div className="bg-slate-900 p-6 rounded-xl border border-slate-700 shadow-lg">
        <h2 className="text-lg font-bold text-cyan-400 mb-4">
          Forensic Intelligence
        </h2>
        <p className="text-slate-400">No data yet.</p>
      </div>
    );
  }

  const deepfake = Number(result.deepfake_score || 0);
  const aiScore = Number(result.ai_score || 0);

  let risk = "LOW";
  let riskColor = "text-green-400";

  if (result.final_verdict === "DEEPFAKE" || result.final_verdict === "AI_GENERATED") {
    risk = "HIGH";
    riskColor = "text-red-400";
  } else if (result.final_verdict === "SUSPICIOUS" || result.final_verdict === "EDITED_OR_FILTERED") {
    risk = "MEDIUM";
    riskColor = "text-yellow-400";
  }

  const verdictColor =
    result.final_verdict === "REAL_CAMERA"
      ? "text-green-400"
      : result.final_verdict === "DEEPFAKE" || result.final_verdict === "AI_GENERATED"
      ? "text-red-400"
      : "text-yellow-400";

  return (
    <div className="bg-slate-900 p-6 rounded-xl border border-slate-700 shadow-lg">
      <h2 className="text-lg font-bold text-cyan-400 mb-4">
        Forensic Intelligence
      </h2>

      <p className="text-white text-lg font-bold">
        Verdict: <span className={verdictColor}>{result.final_verdict}</span>
      </p>

      <p className="mt-2 text-white font-semibold">
        Risk Level: <span className={riskColor}>{risk}</span>
      </p>

      {result.reason && (
        <div className="mt-4 p-3 bg-slate-800/50 rounded-lg border border-slate-700">
          <p className="text-slate-300 text-sm leading-relaxed">
            <span className="font-semibold text-cyan-400">Reasoning: </span> {result.reason}
          </p>
        </div>
      )}

      <div className="mt-5">
        <p className="text-slate-300 text-sm mb-2">
          Deepfake Score: <span className="text-white">{deepfake}</span>
        </p>
        <div className="w-full bg-slate-800 rounded-full h-3">
          <div
            className="bg-red-500 h-3 rounded-full"
            style={{ width: `${deepfake * 100}%` }}
          ></div>
        </div>
      </div>

      <div className="mt-5">
        <p className="text-slate-300 text-sm mb-2">
          AI Artifact Score: <span className="text-white">{aiScore}</span>
        </p>
        <div className="w-full bg-slate-800 rounded-full h-3">
          <div
            className="bg-cyan-500 h-3 rounded-full"
            style={{ width: `${aiScore * 100}%` }}
          ></div>
        </div>
      </div>

      <div className="mt-5">
        <p className="text-slate-400 text-sm">Metadata:</p>
        <p className="text-white text-sm mt-1">{result.metadata}</p>
      </div>

      <div className="mt-6">
        <p className="text-slate-400 text-sm">Evidence Summary:</p>
        <ul className="list-disc ml-5 text-slate-300 text-sm mt-2 space-y-1">
          <li>CNN based face classification applied</li>
          <li>AI artifact texture detection performed</li>
          <li>Metadata & software traces checked</li>
        </ul>
      </div>
    </div>
  );
}
