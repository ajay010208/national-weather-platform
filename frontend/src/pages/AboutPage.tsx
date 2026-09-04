export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto bg-white rounded-2xl shadow-md p-8 border border-slate-100 prose prose-slate">
      <h1 className="text-2xl font-bold text-slate-800 mb-4">About This Platform</h1>
      <p className="text-slate-600 leading-relaxed">
        This is the MVP of the <strong>National Weather Big Data Analytics Platform</strong> built for
        Smart India Hackathon 2026 – Problem 69.
      </p>
      <h2 className="text-lg font-semibold mt-6 mb-2">Current Capabilities (MVP)</h2>
      <ul className="list-disc pl-5 text-slate-600 space-y-1">
        <li>Real-time weather for major Indian cities (Open-Meteo)</li>
        <li>7-day forecast + hourly charts</li>
        <li>Rule-based alerts (heatwave, thunderstorm, UV)</li>
        <li>Interactive map with Leaflet</li>
        <li>Conversational WeatherGPT (rule-based, ready for RAG upgrade)</li>
      </ul>
      <h2 className="text-lg font-semibold mt-6 mb-2">Tech Stack</h2>
      <p className="text-slate-600">
        Backend: FastAPI · Frontend: React + TypeScript + Tailwind · Maps: Leaflet · Charts: Recharts · Data: Open-Meteo
      </p>
    </div>
  )
}
