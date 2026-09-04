from fastapi import APIRouter, Query, HTTPException
from datetime import datetime, timezone
from typing import Optional
from loguru import logger

from app.models.schemas import (
    ForecastResponse, AlertsResponse, HistoricalResponse,
    HealthResponse, ChatRequest, ChatResponse,
)
from app.services.weather_service import (
    resolve_location, get_forecast, get_alerts, get_historical,
    INDIAN_CITIES,
)

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version="1.0.0-mvp",
        timestamp=datetime.now(timezone.utc),
        services={
            "open_meteo": "available",
            "database": "sqlite-ready",
            "models": "rule-based-mvp",
        },
    )

@router.get("/cities")
async def list_cities():
    return {
        "cities": [
            {"key": k, "name": v.name, "state": v.state, "lat": v.latitude, "lon": v.longitude}
            for k, v in INDIAN_CITIES.items()
        ]
    }

@router.get("/weather/current", response_model=ForecastResponse)
async def current_weather(
    city: Optional[str] = Query(None, description="City name e.g. delhi, mumbai"),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
):
    location = resolve_location(city, lat, lon)
    try:
        return await get_forecast(location)
    except Exception as e:
        logger.error(f"Forecast error: {e}")
        raise HTTPException(status_code=502, detail=f"Upstream weather service error: {str(e)}")

@router.get("/forecast", response_model=ForecastResponse)
async def forecast(
    city: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
):
    return await current_weather(city, lat, lon)

@router.get("/alerts", response_model=AlertsResponse)
async def alerts(
    city: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
):
    location = resolve_location(city, lat, lon)
    try:
        return await get_alerts(location)
    except Exception as e:
        logger.error(f"Alerts error: {e}")
        raise HTTPException(status_code=502, detail=str(e))

@router.get("/historical", response_model=HistoricalResponse)
async def historical(
    city: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    start_date: str = Query(..., description="YYYY-MM-DD"),
    end_date: str = Query(..., description="YYYY-MM-DD"),
):
    location = resolve_location(city, lat, lon)
    try:
        return await get_historical(location, start_date, end_date)
    except Exception as e:
        logger.error(f"Historical error: {e}")
        raise HTTPException(status_code=502, detail=str(e))

@router.post("/chat", response_model=ChatResponse)
async def weather_chat(req: ChatRequest):
    msg = req.message.lower()
    location = req.location or resolve_location("delhi")

    if any(w in msg for w in ["temperature", "temp", "hot", "cold", "how is weather", "current"]):
        try:
            forecast = await get_forecast(location)
            cur = forecast.current
            reply = (
                f"In {location.name} right now it is {cur.temperature:.1f}\u00b0C "
                f"({cur.weather_description}). Humidity {cur.humidity:.0f}%, "
                f"wind {cur.wind_speed:.1f} km/h."
            )
            if cur.feels_like:
                reply += f" Feels like {cur.feels_like:.1f}\u00b0C."
            return ChatResponse(reply=reply, sources=["open-meteo"], confidence=0.9)
        except Exception:
            return ChatResponse(reply="Sorry, I couldn't fetch the latest weather data.", confidence=0.3)

    if any(w in msg for w in ["rain", "rainfall", "precipitation", "will it rain"]):
        try:
            forecast = await get_forecast(location)
            next_rain = next((h for h in forecast.hourly if h.precipitation_probability > 40), None)
            if next_rain:
                reply = f"There is a {next_rain.precipitation_probability:.0f}% chance of rain around {next_rain.time.strftime('%H:%M')} today in {location.name}."
            else:
                reply = f"No significant rain expected in the next 48 hours in {location.name}."
            return ChatResponse(reply=reply, sources=["open-meteo"], confidence=0.85)
        except Exception:
            return ChatResponse(reply="Could not check rainfall probability right now.", confidence=0.3)

    if any(w in msg for w in ["alert", "warning", "heatwave", "cyclone", "storm"]):
        try:
            alerts_resp = await get_alerts(location)
            if alerts_resp.count == 0:
                reply = f"No active weather alerts for {location.name} at the moment."
            else:
                parts = [f"\u2022 {a.title}: {a.description}" for a in alerts_resp.alerts]
                reply = f"Active alerts for {location.name}:\n" + "\n".join(parts)
            return ChatResponse(reply=reply, sources=["platform-rules"], confidence=0.8)
        except Exception:
            return ChatResponse(reply="Unable to retrieve alerts.", confidence=0.3)

    reply = (
        "I am WeatherGPT (MVP). I can tell you about current temperature, rain chances, "
        "and active alerts for major Indian cities. Try asking:\n"
        "- What is the temperature in Mumbai?\n"
        "- Will it rain in Delhi today?\n"
        "- Any heatwave alerts in Rajasthan?"
    )
    return ChatResponse(reply=reply, sources=[], confidence=0.7)
