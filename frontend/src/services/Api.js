import axios from "axios";

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");
const api = axios.create({ baseURL: API_BASE_URL, timeout: 15000 });

export const getHealth = async () => (await api.get("/api/health")).data;
export const getMetadata = async () => (await api.get("/api/metadata")).data;
export const getDemoInputs = async () => (await api.get("/api/demo-inputs")).data;
export const getMapForecast = async () => (await api.get("/api/forecast/map")).data;
export const getForecast = async (payload) => (await api.post("/api/forecast", payload)).data;
export const getVerification = async () => (await api.get("/api/verification")).data;
export const getHistory = async (limit = 50) => (await api.get(`/api/predictions?limit=${limit}`)).data;
export { API_BASE_URL };
