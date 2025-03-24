import api from "../utils/api";

export const buy_request = async (stock_name, quantity, stock_price) => {
    try {
        const response = await api.post("/trade/buy_request", {
            stock_name: stock_name,
            stock_price: stock_price,
            quantity: quantity
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

export const get_stock_detail = async (stock_name) => {
    try {
        const response = await api.get(`/get_info/stock_detail/${stock_name}`);
        console.log(response.data);
        return response.data;
    } catch (error) {
        throw error.response?.data?.detail || "주식 상세 조회 실패";
    }
};

export const get_trade_stocks = async (stock_name) => {
    try {
        const response = await api.get(`/get_info/trade_stocks/${stock_name}`);
        return response.data;
    } catch (error) {
        throw error.response?.data?.detail || "주식 매도/매수 조회 실패";
    }
};