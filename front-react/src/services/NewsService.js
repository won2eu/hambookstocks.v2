import api from "../utils/api";

export const get_news = async () => {
    try{
        const response = await api.get("/news");
        return response.data;
    }
    catch(error){
        throw error.response?.data?.detail || "뉴스 가져오기 실패";
    }
}

