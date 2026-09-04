import axios from 'axios';
import type { ForecastResponse, AlertsResponse, City, ChatMessage } from '../types/weather';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const client = axios.create({
  baseURL: API_BASE,
  timeout: 15000,
});

export async function getCities(): Promise<City[]> {
  const { data } = await client.get('/cities');
  return data.cities;
}

export async function getForecast(params: { city?: string; lat?: number; lon?: number }): Promise<ForecastResponse> {
  const { data } = await client.get('/forecast', { params });
  return data;
}

export async function getAlerts(params: { city?: string; lat?: number; lon?: number }): Promise<AlertsResponse> {
  const { data } = await client.get('/alerts', { params });
  return data;
}

export async function sendChat(message: string, location?: { name: string; latitude: number; longitude: number }, history: ChatMessage[] = []) {
  const { data } = await client.post('/chat', { message, location, history });
  return data;
}

export async function healthCheck() {
  const { data } = await client.get('/health');
  return data;
}
