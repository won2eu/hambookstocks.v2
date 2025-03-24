import api from "../utils/api";

export const getMyStocks = async () => {
  try {
    const response = await api.get('/mystocks');
    return response.data.mystocks || [];  // mystocks 배열만 반환
  } catch (error) {
    console.error("Error fetching stock data", error);
    throw error;
  }
};
