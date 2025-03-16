import api from "../utils/api";

export const buy_request = async (stock_name, quantity, stock_price) => {
    try {
        const response = await api.post("/trade/buy_request", {
            stock_name,
            stock_price,
            quantity,
        });
        return response.data; // 리턴값 메시지밖에 없음
    } catch (error) {
        throw error.response?.data?.detail || "구매 요청 실패";
    }
};

export const sell_request = async (stock_name, quantity, price) => {
    try {
        const response = await api.post("/trade/sell_request", {
            stock_name,
            quantity,
            price,
        });
        return response.data; // 리턴값 메시지밖에 없음
    } catch (error) {
        throw error.response?.data?.detail || "매도 요청 실패";
    }
};


export const get_my_balance = async () => {
    try {
        const response = await api.get("/my/balance");
        return response.data;
    } catch (error) {
        throw error.response?.data?.detail || "잔액 조회 실패";
    }
};

