import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // FastAPI 서버 주소
  headers: {
    "Content-Type": "application/json",
  },
});

const publicEndpoints = [
  '/auth/login',
  '/auth/signup',  // 토큰이 필요없는 엔드포인트만 추가해주시길 !
  
];

// 요청 인터셉터: 자동으로 토큰 추가
api.interceptors.request.use((config) => {
  if (publicEndpoints.includes(config.url)) {
    return config;
  }

  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
