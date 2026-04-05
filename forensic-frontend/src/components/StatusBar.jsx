export default function StatusBar() {
  return (
    <div className="bg-slate-900 border-b border-cyan-500 p-4 flex justify-between items-center">
      <h1 className="text-xl font-bold text-cyan-400">
        AI Forensic Command System
      </h1>

      <div className="flex gap-6 text-sm text-slate-400">
        <span className="flex items-center gap-2">
          <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
          System Online
        </span>

        
      </div>
    </div>
  );
}
