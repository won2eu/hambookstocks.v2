document.getElementById('signup-form').addEventListener('submit', function (e) {
    e.preventDefault();
  
    const username = document.getElementById('username').value;
    const loginId = document.getElementById('login-id').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
  
    if (password !== confirmPassword) {
      alert("비밀번호가 일치하지 않습니다.");
      return;
    }

    const userData = {
      name: username,
      login_id: loginId,
      pwd: password
    };
  // 주석 변경 실험 입니다!!!!!!
    fetch('/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message === "User registered successfully") {
          alert("회원가입 성공!");
          window.location.href = '/';  // 로그인 페이지로 리다이렉션
        } else {
          alert("회원가입 실패: " + data.detail);
        }
      })
      .catch((error) => {
        console.error('Error:', error);
        alert("회원가입에 실패했습니다.");
      });
  });
  