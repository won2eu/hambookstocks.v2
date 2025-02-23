import '../styles/LoginBox.css';

export default function LoginBox() {
  return (
    <div className="login-box">
      <h3>로그인</h3>
      <div className="In-login-box">
        <input type="text" placeholder="아이디" />
        <input type="password" placeholder="비밀번호" />
        <button>로그인</button>
      </div>
    </div>
  );
}
