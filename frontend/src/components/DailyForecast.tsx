import type { DailyForecast } from '../types/weather'
import { format, parseISO } from 'date-fns'

interface Props {
  data: DailyForecast[]
}

const weatherEmoji: Record<number, string> = {
  0: '☀️', 1: '🌤️', 2: '⛅', 3: '☁️',
  45: '🌫️', 48: '🌫️',
  51: '🌦️', 53: '🌦️', 55: '🌧️',
  61: '🌧️', 63: '🌧️', 65: '🌧️',
  80: '🌦️', 81: '🌧️', 82: '⛈️',
  95: '⛈️', 96: '⛈️', 99: '⛈️',
}

export default function DailyForecastCards({ data }: Props) {
  return (
    <div className="bg-white rounded-2xl shadow-md p-6 border border-slate-100">
      <h3 className="font-semibold text-slate-700 mb-4">7-Day Forecast</h3>
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
        {data.map((d) => (
          <div key={d.date} className="text-center p-3 rounded-xl bg-slate-50 hover:bg-blue-50 transition">
            <p className="text-xs font-medium text-slate-500">{format(parseISO(d.date), 'EEE')}</p>
            <p className="text-2xl my-1">{weatherEmoji[d.weather_code] || '🌡️'}</p>
            <p className="font-bold text-slate-800">{Math.round(d.temperature_max)}°</p>
            <p className="text-sm text-slate-500">{Math.round(d.temperature_min)}°</p>
            <p className="text-xs text-cyan-600 mt-1">{Math.round(d.precipitation_probability_max)}%</p>
          </div>
        ))}
      </div>
    </div>
  )
}
