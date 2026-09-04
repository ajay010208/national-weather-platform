from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class Location(BaseModel):
    name: str
    latitude: float
    longitude: float
    state: Optional[str] = None
    country: str = "India"

class CurrentWeather(BaseModel):
    location: Location
    temperature: float = Field(..., description="Temperature in °C")
    feels_like: Optional[float] = None
    humidity: float
    pressure: float
    wind_speed: float
    wind_direction: Optional[float] = None
    precipitation: float = 0.0
    weather_code: int
    weather_description: str
    visibility: Optional[float] = None
    uv_index: Optional[float] = None
    timestamp: datetime
    source: str = "open-meteo"

class HourlyForecast(BaseModel):
    time: datetime
    temperature: float
    humidity: float
    precipitation_probability: float
    precipitation: float
    weather_code: int
    wind_speed: float

class DailyForecast(BaseModel):
    date: str
    temperature_max: float
    temperature_min: float
    precipitation_sum: float
    precipitation_probability_max: float
    weather_code: int
    wind_speed_max: float
    sunrise: Optional[str] = None
    sunset: Optional[str] = None

class ForecastResponse(BaseModel):
    location: Location
    current: CurrentWeather
    hourly: List[HourlyForecast]
    daily: List[DailyForecast]
    generated_at: datetime
    platform_version: str = "v1.0-mvp"

class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    SEVERE = "severe"
    EXTREME = "extreme"

class WeatherAlert(BaseModel):
    id: str
    title: str
    description: str
    severity: AlertSeverity
    location: Location
    start_time: datetime
    end_time: Optional[datetime] = None
    event_type: str
    source: str = "platform"

class AlertsResponse(BaseModel):
    location: Location
    alerts: List[WeatherAlert]
    count: int

class HistoricalRequest(BaseModel):
    latitude: float
    longitude: float
    start_date: str
    end_date: str
    variables: List[str] = ["temperature_2m", "precipitation"]

class HistoricalResponse(BaseModel):
    location: Location
    start_date: str
    end_date: str
    data: Dict[str, List[Any]]
    source: str = "open-meteo-archive"

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime
    services: Dict[str, str]

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    location: Optional[Location] = None
    history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    reply: str
    sources: List[str] = []
    confidence: float = 0.8
