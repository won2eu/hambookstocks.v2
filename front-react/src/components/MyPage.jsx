import React, { useEffect, useState } from "react";
import { getMyPage, deleteAccount, gg, changePassword, makeStock } from "../services/MyPageService";
import '../styles/MyPage.css'; // CSS 파일 import

const MyPage = () => {
    const [userData, setUserData] = useState(null);
    const token = localStorage.getItem("token"); // 토큰 가져오기

    // 상태변수
    const [showChangePassword, setShowChangePassword] = useState(false); // 비밀번호 변경 폼 보이기 상태
    const [showStockForm, setShowStockForm] = useState(false);

    // 비밀번호 변경 관련
    const [originPwd, setOriginPwd] = useState("");
    const [newPwd, setNewPwd] = useState("");
    const [checkNewPwd, setCheckNewPwd] = useState("");

    // 주식 상장 관련
    const [stock_name, setStockName] = useState("");
    const [stock_price, setStockPrice] = useState("");
    const [stock_quantity, setStockQuantity] = useState("");
    const [stock_description, setStockDescription] = useState("");


    useEffect(() => {
        getMyPage()
            .then(data => setUserData(data))
            .catch(err => console.error(err));
        }
    , []);

    const handleDeleteAccount = async () => {
        if (window.confirm("정말로 탈퇴하시겠습니까?")) {
            await deleteAccount(token);
            alert("회원 탈퇴 완료");
            localStorage.removeItem("token");
            window.location.href = "/";
        }
    };

    const handleGG = async () => {
        await gg(token);
        alert("GG 완료");
        window.location.reload();
    };

    const handleChangePassword = async () => {
        if (newPwd !== checkNewPwd) {
            alert("새 비밀번호가 일치하지 않습니다.");
            return;
        }
        try {
            await changePassword(originPwd, newPwd, checkNewPwd);
            alert("비밀번호가 변경되었습니다. 다시 로그인해 주세요.");
            localStorage.removeItem("token");
            window.location.href = "/login";
        } catch (error) {
            alert("비밀번호 변경 실패: " + error.response?.data?.message || error.message);
        }
    };

    const handleMakeStock = async () => {
        if (!stock_name || !stock_price || !stock_quantity) {
            alert("모든 필드를 입력하세요.");
            return;
        }
        try {
            const stockData = {
                stock_name: stock_name,
                stock_price: parseFloat(stock_price),
                stock_quantity: parseInt(stock_quantity),
                stock_description: stock_description,
            };
            const response = await makeStock(stockData);
            alert(response.message);

            // 성공하면 입력 필드 초기화 & 새로고침
            setStockName("");
            setStockPrice("");
            setStockQuantity("");
            setStockDescription("");
            setShowStockForm(false);

            // 최신 데이터 가져오기
            const updatedData = await getMyPage();
            setUserData(updatedData);
        } catch (error) {
            alert(error.response?.data?.detail || "주식 상장 실패");
        }
    };


    return (
        <div className="mypage-container">
            <h1>Profile</h1>
            {userData ? (
                <div className="profile-box">
                    <div className="profile-img"></div>
                    <div className="user-info">
                        <p>이름: {userData.name}</p>
                        <p>ID: {userData.login_id}</p>
                        <p>이메일: {userData.email}</p>
                        <p>잔고: {userData.balance} 원</p>
                    </div>
                </div>
            ) : (
                <p>Loading...</p>
            )}
            <div className="buttons-container">
                <button onClick={() => setShowChangePassword(!showChangePassword)}>
                    비밀번호 변경
                </button>
                <button onClick={() => setShowStockForm(!showStockForm)}>
                    내 주식 상장
                </button>
                <button onClick={handleGG}>GG</button>
                <button onClick={handleDeleteAccount}>회원 탈퇴</button>
            </div>
    
            {/* showChangePassword 상태가 true일 때만 폼 표시 */}
            {showChangePassword && (
                <div className="change-password-form">
                    <input
                        type="password"
                        placeholder="현재 비밀번호"
                        value={originPwd}
                        onChange={(e) => setOriginPwd(e.target.value)}
                    />
                    <input
                        type="password"
                        placeholder="새 비밀번호"
                        value={newPwd}
                        onChange={(e) => setNewPwd(e.target.value)}
                    />
                    <input
                        type="password"
                        placeholder="새 비밀번호 확인"
                        value={checkNewPwd}
                        onChange={(e) => setCheckNewPwd(e.target.value)}
                    />
                    <button onClick={handleChangePassword}>변경하기</button>
                </div>
            )}

            {/* 주식 상장 폼 */}
            {showStockForm && (
                <div className="stock-form">
                    <h3>나만의 주식 만들기</h3>
                    <input type="text" placeholder="주식 이름" value={stock_name} onChange={(e) => setStockName(e.target.value)} />
                    <input type="number" placeholder="주식 가격" value={stock_price} onChange={(e) => setStockPrice(e.target.value)} />
                    <input type="number" placeholder="주식 수량" value={stock_quantity} onChange={(e) => setStockQuantity(e.target.value)} />
                    <textarea placeholder="설명 (선택사항)" value={stock_description} onChange={(e) => setStockDescription(e.target.value)} />
                    <button onClick={handleMakeStock}>상장하기</button>
                </div>
            )}    
        </div>
    );
};

export default MyPage;