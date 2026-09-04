import httpx
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.models.schemas import (
    Location, CurrentWeather, HourlyForecast, DailyForecast,
    ForecastResponse, WeatherAlert, AlertSeverity, AlertsResponse,
    HistoricalResponse
)

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

INDIAN_CITIES = {
    "delhi": Location(name="New Delhi", latitude=28.6139, longitude=77.2090, state="Delhi"),
    "mumbai": Location(name="Mumbai", latitude=19.0760, longitude=72.8777, state="Maharashtra"),
    "bengaluru": Location(name="Bengaluru", latitude=12.9716, longitude=77.5946, state="Karnataka"),
    "chennai": Location(name="Chennai", latitude=13.0827, longitude=80.2707, state="Tamil Nadu"),
    "kolkata": Location(name="Kolkata", latitude=22.5726, longitude=88.3639, state="West Bengal"),
    "hyderabad": Location(name="Hyderabad", latitude=17.3850, longitude=78.4867, state="Telangana"),
    "pune": Location(name="Pune", latitude=18.5204, longitude=73.8567, state="Maharashtra"),
    "ahmedabad": Location(name="Ahmedabad", latitude=23.0225, longitude=72.5714, state="Gujarat"),
    "jaipur": Location(name="Jaipur", latitude=26.9124, longitude=75.7873, state="Rajasthan"),
    "lucknow": Location(name="Lucknow", latitude=26.8467, longitude=80.9462, state="Uttar Pradesh"),
    "chandigarh": Location(name="Chandigarh", latitude=30.7333, longitude=76.7794, state="Chandigarh"),
    "bhopal": Location(name="Bhopal", latitude=23.2599, longitude=77.4126, state="Madhya Pradesh"),
    "patna": Location(name="Patna", latitude=25.5941, longitude=85.1376, state="Bihar"),
    "guwahati": Location(name="Guwahati", latitude=26.1445, longitude=91.7362, state="Assam"),
    "thiruvananthapuram": Location(name="Thiruvananthapuram", latitude=8.5241, longitude=76.9366, state="Kerala"),
}

def get_location_by_name(name: str) -> Optional[Location]:
    key = name.lower().strip().replace(" ", "")
    return INDIAN_CITIES.get(key)

def resolve_location(name: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None) -> Location:
    if name:
        loc = get_location_by_name(name)
        if loc:
            return loc
        return Location(name=name, latitude=lat or 28.6139, longitude=lon or 77.2090)
    if lat is not None and lon is not None:
        return Location(name=f"{lat:.2f},{lon:.2f}", latitude=lat, longitude=lon)
    return INDIAN_CITIES["delhi"]

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
async def fetch_open_meteo_forecast(lat: float, lon: float) -> Dict[str, Any]:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,pressure_msl,wind_speed_10m,wind_direction_10m,uv_index",
        "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,weather_code,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,sunrise,sunset",
        "timezone": "Asia/Kolkata",
        "forecast_days": 7,
    }
    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.get(settings.OPEN_METEO_FORECAST_URL, params=params)
        resp.raise_for_status()
        return resp.json()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
async def fetch_open_meteo_historical(lat: float, lon: float, start: str, end: str) -> Dict[str, Any]:
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start,
        "end_date": end,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
        "timezone": "Asia/Kolkata",
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(settings.OPEN_METEO_HISTORICAL_URL, params=params)
        resp.raise_for_status()
        return resp.json()

def parse_current(data: Dict, location: Location) -> CurrentWeather:
    cur = data.get("current", {})
    code = cur.get("weather_code", 0)
    return CurrentWeather(
        location=location,
        temperature=cur.get("temperature_2m", 0.0),
        feels_like=cur.get("apparent_temperature"),
        humidity=cur.get("relative_humidity_2m", 0.0),
        pressure=cur.get("pressure_msl", 1013.0),
        wind_speed=cur.get("wind_speed_10m", 0.0),
        wind_direction=cur.get("wind_direction_10m"),
        precipitation=cur.get("precipitation", 0.0),
        weather_code=code,
        weather_description=WEATHER_CODES.get(code, "Unknown"),
        uv_index=cur.get("uv_index"),
        timestamp=datetime.now(timezone.utc),
        source="open-meteo",
    )

def parse_hourly(data: Dict) -> List[HourlyForecast]:
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    result = []
    for i, t in enumerate(times[:48]):
        result.append(HourlyForecast(
            time=datetime.fromisoformat(t),
            temperature=hourly.get("temperature_2m", [0])[i],
            humidity=hourly.get("relative_humidity_2m", [0])[i],
            precipitation_probability=hourly.get("precipitation_probability", [0])[i],
            precipitation=hourly.get("precipitation", [0])[i],
            weather_code=hourly.get("weather_code", [0])[i],
            wind_speed=hourly.get("wind_speed_10m", [0])[i],
        ))
    return result

def parse_daily(data: Dict) -> List[DailyForecast]:
    daily = data.get("daily", {})
    times = daily.get("time", [])
    result = []
    for i, t in enumerate(times):
        result.append(DailyForecast(
            date=t,
            temperature_max=daily.get("temperature_2m_max", [0])[i],
            temperature_min=daily.get("temperature_2m_min", [0])[i],
            precipitation_sum=daily.get("precipitation_sum", [0])[i],
            precipitation_probability_max=daily.get("precipitation_probability_max", [0])[i],
            weather_code=daily.get("weather_code", [0])[i],
            wind_speed_max=daily.get("wind_speed_10m_max", [0])[i],
            sunrise=daily.get("sunrise", [None])[i] if daily.get("sunrise") else None,
            sunset=daily.get("sunset", [None])[i] if daily.get("sunset") else None,
        ))
    return result

async def get_forecast(location: Location) -> ForecastResponse:
    logger.info(f"Fetching forecast for {location.name} ({location.latitude}, {location.longitude})")
    raw = await fetch_open_meteo_forecast(location.latitude, location.longitude)
    current = parse_current(raw, location)
    hourly = parse_hourly(raw)
    daily = parse_daily(raw)
    return ForecastResponse(
        location=location,
        current=current,
        hourly=hourly,
        daily=daily,
        generated_at=datetime.now(timezone.utc),
    )

async def get_historical(location: Location, start: str, end: str) -> HistoricalResponse:
    logger.info(f"Fetching historical for {location.name} {start} to {end}")
    raw = await fetch_open_meteo_historical(location.latitude, location.longitude, start, end)
    daily = raw.get("daily", {})
    return HistoricalResponse(
        location=location,
        start_date=start,
        end_date=end,
        data={
            "time": daily.get("time", []),
            "temperature_max": daily.get("temperature_2m_max", []),
            "temperature_min": daily.get("temperature_2m_min", []),
            "precipitation": daily.get("precipitation_sum", []),
            "weather_code": daily.get("weather_code", []),
        },
    )

def generate_mock_alerts(location: Location, current: CurrentWeather) -> List[WeatherAlert]:
    alerts = []
    now = datetime.now(timezone.utc)
    if current.temperature >= 40:
        alerts.append(WeatherAlert(
            id=f"heat-{location.name.lower().replace(' ', '-')}-{now.strftime('%Y%m%d')}",
            title="Heatwave Warning",
            description=f"High temperature of {current.temperature:.1f}C recorded. Stay hydrated and avoid outdoor activity during peak hours.",
            severity=AlertSeverity.SEVERE if current.temperature >= 45 else AlertSeverity.WARNING,
            location=location,
            start_time=now,
            event_type="heatwave",
            source="platform-rules",
        ))
    if current.weather_code in [65, 82, 95, 96, 99] or current.precipitation > 10:
        alerts.append(WeatherAlert(
            id=f"storm-{location.name.lower().replace(' ', '-')}-{now.strftime('%Y%m%d%H')}",
            title="Thunderstorm / Heavy Rain Alert",
            description=f"Current conditions indicate possible thunderstorm or heavy rain. Precipitation: {current.precipitation} mm.",
            severity=AlertSeverity.WARNING,
            location=location,
            start_time=now,
            event_type="thunderstorm",
            source="platform-rules",
        ))
    if current.uv_index and current.uv_index >= 8:
        alerts.append(WeatherAlert(
            id=f"uv-{location.name.lower().replace(' ', '-')}-{now.strftime('%Y%m%d')}",
            title="High UV Index",
            description=f"UV Index is {current.uv_index}. Use sunscreen and protective clothing.",
            severity=AlertSeverity.INFO,
            location=location,
            start_time=now,
            event_type="uv",
            source="platform-rules",
        ))
    return alerts

async def get_alerts(location: Location) -> AlertsResponse:
    forecast = await get_forecast(location)
    alerts = generate_mock_alerts(location, forecast.current)
    return AlertsResponse(location=location, alerts=alerts, count=len(alerts))
