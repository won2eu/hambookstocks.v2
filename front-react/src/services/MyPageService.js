import api from "../utils/api"; 

export const getMyPage = async () => {
    try {
        const response = await api.get("/mypage");
        console.log("MyPage API Response:", response.data);
        return response.data;
    } catch (error) {
        console.error("Failed to fetch My Page data:", error);
        throw error;
    }
};

export const deleteAccount = async () => {
    try {
        const response = await api.post("/mypage/delete_account");
        return response.data;
    } catch (error) {
        console.error("Failed to delete account:", error);
        throw error;
    }
};

export const gg = async () => {
    try {
        const response = await api.post("/mypage/gg");
        return response.data;
    } catch (error) {
        console.error("GG request failed:", error);
        throw error;
    }
};

export const changePassword = async (origin_pwd, new_pwd, check_new_pwd) => {
    try {
        const response = await api.post("/mypage/change_pwd", {
            origin_pwd,
            new_pwd,
            check_new_pwd
        });
        return response.data;
    } catch (error) {
        console.error("Password change failed:", error);
        throw error;
    }
};

// 주식 상장
export const makeStock = async (stockData) => {
    try {
        const response = await api.post("/mypage/make_stock", stockData);
        return response.data;
    } catch (error) {
        console.error("Failed to make stock:", error);
        throw error;
    }
};