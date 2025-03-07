import api from "../utils/api";

export const login = async (loginID, password) => {
    try{
        const response = await api.post("/auth/login",{
            login_id: loginID,
            pwd: password
        });
        return response.data;
    } catch(error){
        throw error.response?.data?.detail || "로그인 실패";
    }
};