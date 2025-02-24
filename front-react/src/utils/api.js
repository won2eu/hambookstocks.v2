import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // FastAPI 서버 주소
  headers: {
    "Content-Type": "application/json",
  },
});

// 요청 인터셉터: 자동으로 토큰 추가
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
