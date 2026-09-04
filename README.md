# National Weather Big Data Analytics Platform

**SIH 2026 – Problem 69**  
Full-stack MVP with real-time weather, forecasts, alerts, interactive dashboard, and WeatherGPT.

## Features

- Current weather for 15 major Indian cities (Open-Meteo, no API key)
- Hourly + 7-day forecast with charts
- Interactive map (Leaflet)
- Rule-based alerts (heatwave, thunderstorm, UV)
- WeatherGPT chat assistant
- REST API with Swagger at `/docs`

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API: http://localhost:8000  
Docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open: http://localhost:5173

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/cities` | List cities |
| GET | `/api/v1/forecast?city=delhi` | Current + hourly + daily |
| GET | `/api/v1/alerts?city=mumbai` | Active alerts |
| GET | `/api/v1/historical?city=delhi&start_date=2024-01-01&end_date=2024-01-31` | Historical |
| POST | `/api/v1/chat` | WeatherGPT |

## Tech stack

Backend: FastAPI · Frontend: React + TypeScript + Tailwind · Maps: Leaflet · Charts: Recharts · Data: Open-Meteo

Built for educational / SIH purposes.
