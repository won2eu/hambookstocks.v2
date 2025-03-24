import React, { useEffect, useState, useRef } from 'react';
import { getMyPage, deleteAccount, gg, changePassword, makeStock } from '../services/MyPageService';
import { useNavigate } from 'react-router-dom';
import '../styles/MyPage.css'; 

const MyPage = () => {
  const navigate = useNavigate(); // useNavigate 사용
  const [userData, setUserData] = useState(null);
  const token = localStorage.getItem('token'); // 토큰 가져오기
  const hasAlerted = useRef(false); // 중복 실행 방지

  // 상태변수
  const [showChangePassword, setShowChangePassword] = useState(false); 
  const [showStockForm, setShowStockForm] = useState(false);

  // 비밀번호 변경 관련
  const [originPwd, setOriginPwd] = useState('');
  const [newPwd, setNewPwd] = useState('');
  const [checkNewPwd, setCheckNewPwd] = useState('');

  // 주식 상장 관련
  const [stock_name, setStockName] = useState('');
  const [stock_price, setStockPrice] = useState('');
  const [stock_quantity, setStockQuantity] = useState('');
  const [stock_description, setStockDescription] = useState('');

  useEffect(() => {
    if (!token) {
      if (!hasAlerted.current) {
        hasAlerted.current = true;
        alert('로그인이 필요한 페이지입니다.');
      }
      navigate('/');
      return; // return 추가 -> `getMyPage()`가 실행되지 않도록 함
    }
  
    getMyPage()
      .then((data) => setUserData(data))
      .catch((err) => console.error('데이터 로드 오류:', err));
  }, [navigate, token]);

  // 폼 상태 토글 함수
  const handleToggleForm = (formType) => {
    // 선택된 폼을 보이게 하고, 다른 폼은 숨김
    if (formType === 'password') {
      setShowChangePassword(!showChangePassword); // 상태 변수 반전
      setShowStockForm(false); // 주식 상장 폼 숨기기
    } else if (formType === 'stock') {
      setShowStockForm(!showStockForm);
      setShowChangePassword(false); // 비밀번호 변경 폼 숨기기
    }
  };

  const handleDeleteAccount = async () => {
    if (window.confirm('정말로 탈퇴하시겠습니까?')) {
      await deleteAccount(token);
      alert('회원 탈퇴 완료');
      localStorage.removeItem('token');
      window.location.href = '/';
    }
  };

  const handleGG = async () => {
    if (window.confirm('정말로 ㅈㅈ하시겠습니까?')) {
      await gg(token);
      alert('GG 완료! 당신의 앞날을 응원합니다.');
      window.location.reload();
    }
  };

  const handleChangePassword = async () => {
    if (newPwd !== checkNewPwd) {
      alert('새 비밀번호가 일치하지 않습니다.');
      return;
    }
    try {
      await changePassword(originPwd, newPwd, checkNewPwd);
      alert('비밀번호가 변경되었습니다. 다시 로그인해 주세요.');
      localStorage.removeItem('token');
      window.location.href = '/login';
    } catch (error) {
      alert('비밀번호 변경 실패: ' + error.response?.data?.message || error.message);
    }
  };

  const handleMakeStock = async () => {
    if (!stock_name || !stock_price || !stock_quantity) {
      alert('모든 필드를 입력하세요.');
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
      setStockName('');
      setStockPrice('');
      setStockQuantity('');
      setStockDescription('');
      setShowStockForm(false);

      // 최신 데이터 가져오기
      const updatedData = await getMyPage();
      setUserData(updatedData);
    } catch (error) {
      alert(error.response?.data?.detail || '주식 상장 실패');
    }
  };

  return (
    <div className="mypage-container">
      <h1>Profile</h1>
      {userData ? (
        <div className="profile-box">
        <div className="profile-img">
          {/* 이미지 삽입 */}
          <img src="/user.png" alt="Profile"/>
        </div>
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
        <button className="change-pw-btn" onClick={() => handleToggleForm('password')}>비밀번호 변경</button>
        <button className="make-stock-btn" onClick={() => handleToggleForm('stock')}>내 주식 상장</button>
        <button className="gg-btn" onClick={handleGG}>GG</button>
        <button className="delete-btn" onClick={handleDeleteAccount}>회원 탈퇴</button>
      </div>

      {/* 비밀번호 변경 폼 */}
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
          <input
            type="text"
            placeholder="주식 이름"
            value={stock_name}
            onChange={(e) => setStockName(e.target.value)}
          />
          <input
            type="number"
            placeholder="주식 가격"
            value={stock_price}
            onChange={(e) => setStockPrice(e.target.value)}
          />
          <input
            type="number"
            placeholder="주식 수량"
            value={stock_quantity}
            onChange={(e) => setStockQuantity(e.target.value)}
          />
          <textarea
            placeholder="설명 (선택사항)"
            value={stock_description}
            onChange={(e) => setStockDescription(e.target.value)}
          />
          <button onClick={handleMakeStock}>상장하기</button>
        </div>
      )}
    </div>
  );
};

export default MyPage;
