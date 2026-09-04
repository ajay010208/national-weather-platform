import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import type { Location } from '../types/weather'
import L from 'leaflet'

const DefaultIcon = L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
})
L.Marker.prototype.options.icon = DefaultIcon

interface Props {
  location: Location
  temperature?: number
}

export default function WeatherMap({ location, temperature }: Props) {
  return (
    <div className="bg-white rounded-2xl shadow-md overflow-hidden border border-slate-100 h-72">
      <MapContainer
        center={[location.latitude, location.longitude]}
        zoom={10}
        scrollWheelZoom={false}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={[location.latitude, location.longitude]}>
          <Popup>
            <strong>{location.name}</strong>
            {temperature !== undefined && <br />}
            {temperature !== undefined && `${temperature.toFixed(1)}°C`}
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  )
}
