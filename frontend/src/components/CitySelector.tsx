import { useEffect, useState } from 'react'
import { getCities } from '../services/api'
import type { City } from '../types/weather'
import { MapPin } from 'lucide-react'

interface Props {
  selected: string
  onChange: (cityKey: string) => void
}

export default function CitySelector({ selected, onChange }: Props) {
  const [cities, setCities] = useState<City[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getCities()
      .then(setCities)
      .catch(() => {
        setCities([
          { key: 'delhi', name: 'New Delhi', state: 'Delhi', lat: 28.61, lon: 77.21 },
          { key: 'mumbai', name: 'Mumbai', state: 'Maharashtra', lat: 19.08, lon: 72.88 },
          { key: 'bengaluru', name: 'Bengaluru', state: 'Karnataka', lat: 12.97, lon: 77.59 },
          { key: 'chennai', name: 'Chennai', state: 'Tamil Nadu', lat: 13.08, lon: 80.27 },
          { key: 'kolkata', name: 'Kolkata', state: 'West Bengal', lat: 22.57, lon: 88.36 },
          { key: 'hyderabad', name: 'Hyderabad', state: 'Telangana', lat: 17.39, lon: 78.49 },
        ])
      })
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="flex items-center gap-2">
      <MapPin className="w-5 h-5 text-blue-600" />
      <select
        value={selected}
        onChange={(e) => onChange(e.target.value)}
        disabled={loading}
        className="bg-white border border-slate-300 rounded-lg px-3 py-2 text-sm font-medium shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        {cities.map((c) => (
          <option key={c.key} value={c.key}>
            {c.name}{c.state ? `, ${c.state}` : ''}
          </option>
        ))}
      </select>
    </div>
  )
}
