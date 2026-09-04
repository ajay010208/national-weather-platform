import type { CurrentWeather } from '../types/weather'
import { Droplets, Wind, Gauge, Sun } from 'lucide-react'

interface Props {
  data: CurrentWeather
}

export default function CurrentCard({ data }: Props) {
  return (
    <div className="bg-white rounded-2xl shadow-md p-6 border border-slate-100">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-800">{data.location.name}</h2>
          <p className="text-slate-500 text-sm mt-1">{data.weather_description}</p>
        </div>
        <div className="text-right">
          <div className="text-5xl font-bold text-blue-600">{data.temperature.toFixed(1)}°</div>
          {data.feels_like !== undefined && (
            <p className="text-sm text-slate-500">Feels like {data.feels_like.toFixed(1)}°</p>
          )}
        </div>
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6">
        <div className="flex items-center gap-2">
          <Droplets className="w-5 h-5 text-blue-400" />
          <div>
            <p className="text-xs text-slate-500">Humidity</p>
            <p className="font-semibold">{data.humidity.toFixed(0)}%</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Wind className="w-5 h-5 text-slate-400" />
          <div>
            <p className="text-xs text-slate-500">Wind</p>
            <p className="font-semibold">{data.wind_speed.toFixed(1)} km/h</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Gauge className="w-5 h-5 text-purple-400" />
          <div>
            <p className="text-xs text-slate-500">Pressure</p>
            <p className="font-semibold">{data.pressure.toFixed(0)} hPa</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Sun className="w-5 h-5 text-amber-400" />
          <div>
            <p className="text-xs text-slate-500">UV Index</p>
            <p className="font-semibold">{data.uv_index?.toFixed(1) ?? '—'}</p>
          </div>
        </div>
      </div>
    </div>
  )
}
