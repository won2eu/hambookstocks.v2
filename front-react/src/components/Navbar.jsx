import { useState, useEffect } from 'react';
import { login } from '../services/authservice';
import '../styles/Navbar.css';
import { signup } from '../services/authservice';

export default function Navbar() {
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [isSignUpMode, setIsSignUpMode] = useState(false);
  const [loginID, setLoginId] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');

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

  const handleLogin = async () => {
    try {
      if (!loginID || !password) {
        setError('모든 칸을 입력해주세요.');
        return;
      }
      const responseData = await login(loginID, password);
      localStorage.setItem('token', responseData.access_token);
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

  return (
    <nav className="navbar">
      <div className="logo">HAMBOOK-STOCKS</div>
      <div className="menu">
        <a href="/" className="menu-item">
          Home
        </a>
        <a href="/about" className="menu-item">
          How To Play
        </a>
        <a href="/MyPage" className="menu-item">
          MyPage
        </a>
        <button className="menu-item" onClick={toggleLoginPanel}>
          Login
        </button>
      </div>

      {isLoginOpen && (
        <div className="login-panel open">
          {!isSignUpMode ? (
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
          )}
        </div>
      )}

      {isLoginOpen && <div className="overlay" onClick={toggleLoginPanel}></div>}
    </nav>
  );
}
