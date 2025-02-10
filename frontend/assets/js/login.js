document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault();
  
    const loginId = document.getElementById('login-id').value;
    const password = document.getElementById('password').value;
  
    const loginData = {
      login_id: loginId,
      pwd: password
    };
  
    fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(loginData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message === "로그인 되었습니다.") {
          alert("로그인 성공!");
          window.location.href = 'dashboard.html';  // 대시보드 페이지로 리다이렉션
        } else {
          alert("로그인 실패: " + data.message);
        }
      })
      .catch((error) => {
        console.error('Error:', error);
        alert("로그인에 실패했습니다.");
      });
  });
  