import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

  export const getMapForecast = async () => {
  const response = await axios.get(
    `${API_BASE_URL}/api/forecast/map`
  );

  return response.data;
};

export const getForecast = async (payload) => {
  const response = await axios.post(
    `${API_BASE_URL}/api/forecast`,
    payload
  );

  return response.data;
};

export const getVerification = async () => {
  const response = await axios.get(
    `${API_BASE_URL}/api/verification`
  );

  return response.data;
};

