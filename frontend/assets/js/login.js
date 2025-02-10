document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault();
  
    const loginId = document.getElementById('login-id').value;
    const password = document.getElementById('password').value;
  
    const loginData = {
      login_id: loginId,
      password: password,
    };
  
    fetch('/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(loginData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
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
  