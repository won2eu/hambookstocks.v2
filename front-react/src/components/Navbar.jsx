import { useState, useEffect } from 'react';
import { login } from '../services/authservice';
import '../styles/Navbar.css';
import { signup } from '../services/authservice';
import { logout } from '../services/authservice';
import { Link } from 'react-router-dom'; // Link 추가

export default function Navbar() {
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [isSignUpMode, setIsSignUpMode] = useState(false);
  const [loginID, setLoginId] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false); // 로그인 상태
  const [userName, setUserName] = useState(''); // 로그인 사용자 이름
  const [isGameExplainOpen, setIsGameExplainOpen] = useState(false);
  // 로그인 상태를 체크하는 useEffect
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsLoggedIn(true);
      setUserName(localStorage.getItem('userName')); // 토큰이 있으면 사용자 이름 설정
    }
  }, []);

  const toggleLoginPanel = () => {
    setIsLoginOpen(!isLoginOpen);
    setIsSignUpMode(false);
    resetForm();
  };

  const toggleSignUpMode = () => {
    setIsSignUpMode(!isSignUpMode);
    resetForm();
  };

  const resetForm = () => {
    setLoginId('');
    setPassword('');
    setName('');
    setEmail('');
    setError('');
  };

  const OpenGameExplain = (e) => {
    e.preventDefault();
    setIsGameExplainOpen(!isGameExplainOpen);
  };

  const handleLogin = async () => {
    try {
      if (!loginID || !password) {
        setError('모든 칸을 입력해주세요.');
        return;
      }
      const responseData = await login(loginID, password);
      localStorage.setItem('token', responseData.access_token);
      localStorage.setItem('userName', loginID); // 사용자 이름 저장
      setIsLoggedIn(true); // 로그인 상태 업데이트
      setUserName(loginID); // 사용자 이름 설정
      alert('로그인 성공');
      setIsLoginOpen(false);
      resetForm();
    } catch (err) {
      setError(err.response?.data?.detail || '로그인 실패! 다시 시도해주세요.');
    }
  };

  const handleSignUp = async () => {
    if (!loginID || !password || !name || !email) {
      setError('모든 칸을 입력해주세요.');
      return;
    }

    // const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // if (!emailRegex.test(email)) {
    //   setError('올바른 이메일 형식이 아닙니다.');
    //   return;
    // }

    try {
      const responseData = await signup(loginID, password, name, email);
      alert('회원가입 성공');
      setIsSignUpMode(false);
      resetForm();
    } catch (err) {
      setError(err.response?.data?.detail || '회원가입 실패! 다시 시도해주세요.');
    }
  };

  const handleLogout = async () => {
    try {
      await logout(); // 백엔드에 로그아웃 요청
    } catch (error) {
      console.error('로그아웃 실패:', error);
      alert('로그아웃 중 오류가 발생했습니다.');
    } finally {
      localStorage.removeItem('token'); // 저장된 토큰 삭제
      localStorage.removeItem('userName'); // 사용자 이름 삭제
      setIsLoginOpen(true);
      setUserName('');
      setIsLoggedIn(false);
      alert('로그아웃 되었습니다.');
    }
  };

  return (
    <nav className="navbar">
      <div className="logo">HAMBOOK-STOCKS</div>
      <div className="menu">
        <a href="/" className="menu-item">
          Home
        </a>
        <a href="#" className="menu-item" onClick={OpenGameExplain}>
          How To Play
        </a>
        {isGameExplainOpen && (
          <div className="game-explain">
            <p>1. 주식을 사고팝니다.</p>
            <p>2. 시장 상황을 분석합니다.</p>
            <p>3. 수익을 극대화하세요!</p>
            <p>4. 나만의 주식을 상장해보세요!</p>
          </div>
        )}
        <Link to="/mypage" className="menu-item">
          MyPage
        </Link>{' '}
        {/* link로 수정 */}
        <button className="menu-item" onClick={toggleLoginPanel}>
          {isLoggedIn ? 'My Account' : 'Login'} {/* 로그인 여부에 따라 버튼 이름 변경 */}
        </button>
      </div>

      {isLoginOpen && (
        <div className="login-panel open">
          {!isLoggedIn /* 로그인 여부에 따라 판넬 내용 변경 */ ? (
            !isSignUpMode ? (
              <div className="login-content">
                <p>Please Login Here</p>
                {error && <p className="error-message">{error}</p>}
                <input
                  type="text"
                  placeholder="아이디"
                  value={loginID}
                  onChange={(e) => setLoginId(e.target.value)}
                />
                <input
                  type="password"
                  placeholder="비밀번호"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <button className="login-button" onClick={handleLogin}>
                  Login
                </button>
                <button className="sign-up-box" onClick={toggleSignUpMode}>
                  Sign up
                </button>
              </div>
            ) : (
              <div className="sign-up-content">
                <p>SIGN UP FORM</p>
                {error && <p className="error-message">{error}</p>}
                <input
                  type="text"
                  placeholder="사용할 아이디"
                  value={loginID}
                  onChange={(e) => setLoginId(e.target.value)}
                />
                <input
                  type="password"
                  placeholder="사용할 비밀번호"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <input
                  type="text"
                  placeholder="이름"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
                <input
                  type="email"
                  placeholder="이메일"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
                <button className="sign-up-button" onClick={handleSignUp}>
                  회원가입 하기
                </button>
                <button className="back-to-login" onClick={toggleSignUpMode}>
                  로그인으로 돌아가기
                </button>
              </div>
            )
          ) : (
            <div className="logged-in-content">
              {' '}
              {/* 로그인 성공 시 판넬 내용 변경 */}
              <p>{userName}님 환영합니다!</p>
              <button className="logout-button" onClick={handleLogout}>
                Logout
              </button>
            </div>
          )}
        </div>
      )}

      {isLoginOpen && <div className="overlay" onClick={toggleLoginPanel}></div>}
    </nav>
  );
}
