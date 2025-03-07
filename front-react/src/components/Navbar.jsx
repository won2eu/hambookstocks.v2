import { useState } from 'react';
import '../styles/Navbar.css';

export default function Navbar() {
  const [isLoginOpen, setIsLoginOpen] = useState(false);

  const toggleLoginPanel = () => {
    setIsLoginOpen(!isLoginOpen);
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
      <div className={`login-panel ${isLoginOpen ? 'open' : ''}`}>
        <div className="login-content">
          <p>Please Login Here</p>
          <input type="text" placeholder="아이디" />
          <input type="password" placeholder="비밀번호" />
          <button>Login</button>

          {/* 회원가입 버튼 추가 */}
          <button className="sign-up-box">Sign up</button>
        </div>
      </div>

      {isLoginOpen && <div className="overlay" onClick={toggleLoginPanel}></div>}
    </nav>
  );
}
