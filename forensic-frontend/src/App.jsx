import { useState } from "react";
import StatusBar from "./components/StatusBar";
import UploadPanel from "./components/UploadPanel";
import Scanner from "./components/Scanner";
import ForensicPanel from "./components/ForensicPanel";
import LogsPanel from "./components/logspanel";

export default function App() {
  const [result, setResult] = useState(null);
  const [scanning, setScanning] = useState(false);
  async function analyze() {
  const file = document.getElementById("file").files[0];
  if (!file) return alert("Select image");

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("/analyze", {
    method: "POST",
    body: formData
  });
}

  return (
    <div className="min-h-screen bg-slate-950 text-white relative overflow-hidden">
      
      {/* Background Glow */}
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 via-slate-950 to-purple-500/10 blur-2xl"></div>

      {/* Grid Overlay */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#0f172a_1px,transparent_1px),linear-gradient(to_bottom,#0f172a_1px,transparent_1px)] bg-[size:60px_60px] opacity-20"></div>

      <div className="relative z-10">
        <StatusBar />

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-6">
          
          {/* Left */}
          <UploadPanel setResult={setResult} setScanning={setScanning} />

          {/* Middle */}
          <div className="space-y-6">
            <Scanner result={result} scanning={scanning} />
            <LogsPanel scanning={scanning} result={result} />
          </div>

          {/* Right */}
          <ForensicPanel result={result} />

        </div>
      </div>
    </div>
  );
}
