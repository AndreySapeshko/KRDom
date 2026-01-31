import axios from "axios";
import { getInitData } from "../tg/telegram";

export const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 20000,
});

http.interceptors.request.use((config) => {
  const initData = getInitData();
  if (initData) {
    config.headers = config.headers ?? {};
    config.headers["X-Telegram-InitData"] = initData;
  }
  return config;
});
