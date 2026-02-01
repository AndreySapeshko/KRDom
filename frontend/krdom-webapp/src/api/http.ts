import axios from "axios";
import { getInitData } from "../tg/telegram";

export const http = axios.create({
  baseURL: "/api/v1",
  timeout: 20000,
});

http.interceptors.request.use((config) => {
  const initData = getInitData();

  if (initData) {
    config.headers["X-Telegram-InitData"] = initData;
  }

  return config;
});

http.interceptors.request.use((config) => {
  const initData = getInitData();
  if (initData) {
    config.headers = config.headers ?? {};
    config.headers["X-Telegram-InitData"] = initData;
  }
  return config;
});
