import { Outlet, NavLink } from 'react-router-dom'
import { Cloud, MessageSquare, Info, Activity } from 'lucide-react'

export default function Layout() {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <header className="bg-gradient-to-r from-blue-700 to-blue-900 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <Cloud className="w-8 h-8" />
              <div>
                <h1 className="text-lg font-bold leading-tight">National Weather Platform</h1>
                <p className="text-xs text-blue-200">SIH 2026 · Problem 69</p>
              </div>
            </div>
            <nav className="flex items-center gap-1">
              <NavLink
                to="/"
                end
                className={({ isActive }) =>
                  `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition ${
                    isActive ? 'bg-white/20' : 'hover:bg-white/10'
                  }`
                }
              >
                <Activity className="w-4 h-4" />
                Dashboard
              </NavLink>
              <NavLink
                to="/chat"
                className={({ isActive }) =>
                  `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition ${
                    isActive ? 'bg-white/20' : 'hover:bg-white/10'
                  }`
                }
              >
                <MessageSquare className="w-4 h-4" />
                WeatherGPT
              </NavLink>
              <NavLink
                to="/about"
                className={({ isActive }) =>
                  `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition ${
                    isActive ? 'bg-white/20' : 'hover:bg-white/10'
                  }`
                }
              >
                <Info className="w-4 h-4" />
                About
              </NavLink>
            </nav>
          </div>
        </div>
      </header>
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <Outlet />
      </main>
      <footer className="bg-slate-800 text-slate-300 text-center text-sm py-4">
        <p>Built for Smart India Hackathon 2026 · National Weather Big Data Analytics Platform</p>
        <p className="text-xs text-slate-500 mt-1">MVP · Data powered by Open-Meteo</p>
      </footer>
    </div>
  )
}
