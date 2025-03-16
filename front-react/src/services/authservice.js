import api from "../utils/api";

export const login = async (loginID, password) => {
    try{
        const response = await api.post("/auth/login",{
            login_id: loginID,
            pwd: password
        });
        localStorage.setItem('login_id', loginID);
        window.location.reload();
        return response.data;
    } catch(error){
        throw error.response?.data?.detail || "로그인 실패";
    }
};
export const signup = async (loginID, password, name, email) => {
    try{
        const response = await api.post("/auth/register",{
            login_id: loginID,
            pwd: password,
            name: name,
            email: email
        });
        return response.data;
    } catch(error){
        throw error.response?.data?.detail || "회원가입 실패";
    }
}

export const logout = async () => {
    try {
        const response = await api.post("/auth/logout");
        window.location.reload();
        return response.data;
    } catch (error) {
        throw error.response?.data?.detail || "로그아웃 실패";
    }
};

