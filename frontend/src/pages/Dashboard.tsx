import { useState, useEffect } from 'react'
import CitySelector from '../components/CitySelector'
import CurrentCard from '../components/CurrentCard'
import AlertsPanel from '../components/AlertsPanel'
import HourlyChart from '../components/HourlyChart'
import DailyForecastCards from '../components/DailyForecast'
import WeatherMap from '../components/WeatherMap'
import { getForecast, getAlerts } from '../services/api'
import type { ForecastResponse, AlertsResponse } from '../types/weather'
import { Loader2, RefreshCw } from 'lucide-react'

export default function Dashboard() {
  const [city, setCity] = useState('delhi')
  const [forecast, setForecast] = useState<ForecastResponse | null>(null)
  const [alerts, setAlerts] = useState<AlertsResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadData = async () => {
    setLoading(true)
    setError(null)
    try {
      const [f, a] = await Promise.all([
        getForecast({ city }),
        getAlerts({ city }),
      ])
      setForecast(f)
      setAlerts(a)
    } catch (err: any) {
      setError(err?.message || 'Failed to load weather data. Is the backend running?')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [city])

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <CitySelector selected={city} onChange={setCity} />
        <button
          onClick={loadData}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50 transition"
        >
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <RefreshCw className="w-4 h-4" />}
          Refresh
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl">
          <p className="font-medium">Error</p>
          <p className="text-sm">{error}</p>
          <p className="text-xs mt-1">Make sure the backend is running on port 8000.</p>
        </div>
      )}

      {loading && !forecast && (
        <div className="flex items-center justify-center py-20 text-slate-500">
          <Loader2 className="w-8 h-8 animate-spin mr-3" />
          Loading weather data…
        </div>
      )}

      {forecast && (
        <>
          <div className="grid lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <CurrentCard data={forecast.current} />
            </div>
            <div>
              <AlertsPanel alerts={alerts?.alerts || []} />
            </div>
          </div>
          <div className="grid lg:grid-cols-2 gap-6">
            <HourlyChart data={forecast.hourly} />
            <WeatherMap location={forecast.location} temperature={forecast.current.temperature} />
          </div>
          <DailyForecastCards data={forecast.daily} />
        </>
      )}
    </div>
  )
}
