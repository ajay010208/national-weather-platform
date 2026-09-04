import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts'
import type { HourlyForecast } from '../types/weather'
import { format } from 'date-fns'

interface Props {
  data: HourlyForecast[]
}

export default function HourlyChart({ data }: Props) {
  const chartData = data.slice(0, 24).map((h) => ({
    time: format(new Date(h.time), 'HH:mm'),
    temp: Math.round(h.temperature * 10) / 10,
    precip: h.precipitation_probability,
  }))

  return (
    <div className="bg-white rounded-2xl shadow-md p-6 border border-slate-100">
      <h3 className="font-semibold text-slate-700 mb-4">Next 24 Hours</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="tempGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis dataKey="time" tick={{ fontSize: 11 }} interval={3} />
            <YAxis yAxisId="temp" tick={{ fontSize: 11 }} unit="°" />
            <YAxis yAxisId="precip" orientation="right" tick={{ fontSize: 11 }} unit="%" />
            <Tooltip
              contentStyle={{ borderRadius: 8, border: '1px solid #e2e8f0' }}
              formatter={(value: number, name: string) => [
                name === 'temp' ? `${value}°C` : `${value}%`,
                name === 'temp' ? 'Temperature' : 'Rain chance',
              ]}
            />
            <Area yAxisId="temp" type="monotone" dataKey="temp" stroke="#3b82f6" fill="url(#tempGrad)" strokeWidth={2} />
            <Area yAxisId="precip" type="monotone" dataKey="precip" stroke="#06b6d4" fill="transparent" strokeWidth={1.5} strokeDasharray="4 2" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
