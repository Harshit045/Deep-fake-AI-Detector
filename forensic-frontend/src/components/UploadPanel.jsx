import { useState } from "react";
import axios from "axios";

export default function UploadPanel({ setResult, setScanning }) {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    setFile(selected);

    if (selected) {
      setPreview(URL.createObjectURL(selected));
    }
  };

  const handleAnalyze = async () => {
    if (!file) return alert("Upload an image first!");

    // beep sound
    try {
      const beep = new Audio("/beep.mp3");
      beep.play();
    } catch (err) {}

    setScanning(true);
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("/analyze", formData);
      setResult(res.data);
    } catch (err) {
      alert("Backend not running / API error!");
    }

    setLoading(false);
    setScanning(false);
  };

  return (
    <div className="bg-slate-900 p-6 rounded-xl border border-slate-700 shadow-lg">
      <h2 className="text-lg font-bold text-cyan-400 mb-4">
        Upload Image
      </h2>

      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="text-white"
      />

      {preview && (
        <img
          src={preview}
          alt="preview"
          className="mt-4 w-full h-48 object-cover rounded-lg border border-slate-600"
        />
      )}

      <button
        onClick={handleAnalyze}
        disabled={loading}
        className="mt-4 w-full bg-cyan-500 hover:bg-cyan-600 disabled:bg-slate-600 text-black font-bold py-2 rounded-lg"
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>
    </div>
  );
}
