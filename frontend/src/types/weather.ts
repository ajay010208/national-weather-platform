export interface Location {
  name: string;
  latitude: number;
  longitude: number;
  state?: string;
  country?: string;
}

export interface CurrentWeather {
  location: Location;
  temperature: number;
  feels_like?: number;
  humidity: number;
  pressure: number;
  wind_speed: number;
  wind_direction?: number;
  precipitation: number;
  weather_code: number;
  weather_description: string;
  visibility?: number;
  uv_index?: number;
  timestamp: string;
  source: string;
}

export interface HourlyForecast {
  time: string;
  temperature: number;
  humidity: number;
  precipitation_probability: number;
  precipitation: number;
  weather_code: number;
  wind_speed: number;
}

export interface DailyForecast {
  date: string;
  temperature_max: number;
  temperature_min: number;
  precipitation_sum: number;
  precipitation_probability_max: number;
  weather_code: number;
  wind_speed_max: number;
  sunrise?: string;
  sunset?: string;
}

export interface ForecastResponse {
  location: Location;
  current: CurrentWeather;
  hourly: HourlyForecast[];
  daily: DailyForecast[];
  generated_at: string;
  model_version: string;
}

export interface WeatherAlert {
  id: string;
  title: string;
  description: string;
  severity: 'info' | 'warning' | 'severe' | 'extreme';
  location: Location;
  start_time: string;
  end_time?: string;
  event_type: string;
  source: string;
}

export interface AlertsResponse {
  location: Location;
  alerts: WeatherAlert[];
  count: number;
}

export interface City {
  key: string;
  name: string;
  state?: string;
  lat: number;
  lon: number;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}
