import { useState } from 'react';
import { login } from '../services/authservice';
import '../styles/Navbar.css';

export default function Navbar() {
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [loginID, setLoginId] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const toggleLoginPanel = () => {
    setIsLoginOpen(!isLoginOpen);
  };

  const handleLogin = async () => {
    try {
      const token = await login(loginID, password);
      localStorage.setItem('token', token.access_token);
      alert('로그인 성공');
      setIsLoginOpen(false);
    } catch (err) {
      setError(err.response?.data?.detail || '로그인 실패! 다시 시도해주세요.');
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
        <a href="/services" className="menu-item">
          MyPage
        </a>
        <button className="menu-item" onClick={toggleLoginPanel}>
          Login
        </button>
      </div>

      {isLoginOpen && (
        <div className="login-panel open">
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
          </div>
        </div>
      )}

      {isLoginOpen && <div className="overlay" onClick={toggleLoginPanel}></div>}
    </nav>
  );
}
