import type { WeatherAlert } from '../types/weather'
import { AlertTriangle, Info, AlertCircle } from 'lucide-react'

interface Props {
  alerts: WeatherAlert[]
}

const severityStyles = {
  info: 'bg-blue-50 border-blue-200 text-blue-800',
  warning: 'bg-amber-50 border-amber-200 text-amber-800',
  severe: 'bg-orange-50 border-orange-200 text-orange-800',
  extreme: 'bg-red-50 border-red-200 text-red-800',
}

const severityIcons = {
  info: Info,
  warning: AlertTriangle,
  severe: AlertCircle,
  extreme: AlertCircle,
}

export default function AlertsPanel({ alerts }: Props) {
  if (alerts.length === 0) {
    return (
      <div className="bg-white rounded-2xl shadow-md p-6 border border-slate-100 text-center text-slate-500">
        <Info className="w-8 h-8 mx-auto mb-2 text-green-500" />
        <p className="font-medium">No active weather alerts</p>
        <p className="text-sm">Conditions are currently normal for this location.</p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      <h3 className="font-semibold text-slate-700 flex items-center gap-2">
        <AlertTriangle className="w-5 h-5 text-amber-500" />
        Active Alerts ({alerts.length})
      </h3>
      {alerts.map((alert) => {
        const Icon = severityIcons[alert.severity] || AlertTriangle
        return (
          <div key={alert.id} className={`rounded-xl border p-4 ${severityStyles[alert.severity]}`}>
            <div className="flex items-start gap-3">
              <Icon className="w-5 h-5 mt-0.5 shrink-0" />
              <div>
                <p className="font-semibold">{alert.title}</p>
                <p className="text-sm mt-1 opacity-90">{alert.description}</p>
                <p className="text-xs mt-2 opacity-70 uppercase tracking-wide">{alert.event_type}</p>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
