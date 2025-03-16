# HAMBOOK STOCKS 📈


## [PNU PROJECT] 모의 주식상장 및 투자 게임 서비스

HAMBOOK STOCKS는 주식 투자와 시장 환경을 가상으로 체험할 수 있는 모의 투자 플랫폼입니다.  
직관적인 UI와 강력한 백엔드 서버를 통해 실제 투자 환경을 실감나게 제공합니다.  
실제 주식의 진입 장벽이 높아 실제의 돈으로 선뜻 발을 딛기 어려운 사람들을 위해 가상 머니로 쉽고 더 다이나믹한 가격 변동을 체험할 수 있는 주식 환경을 개발함.

---

## 🔨 기술 스택

### Frontend
- React
- Axios
  
### Backend
- FastAPI

### DataBase
- MySQL
- Redis
---

## 📂 디렉토리 구조
*app directory -> BACKEND

```
hambookstocks.v2
├─ app
│  ├─ dependencies
│  │  ├─ db.py
│  │  ├─ jwt_utils.py
│  │  ├─ redis_db.py
│  │  └─ __init__.py
│  ├─ models
│  │  ├─ DB_Market_stocks_models.py
│  │  ├─ DB_mystocks_models.py
│  │  ├─ DB_trade_models.py
│  │  ├─ DB_user_models.py
│  │  ├─ DB_User_stocks_models.py
│  │  ├─ parameter_models.py
│  │  ├─ stock_model.py
│  │  └─ __init__.py
│  ├─ routers
│  │  ├─ auth_routers.py
│  │  ├─ getnews_routers.py
│  │  ├─ make_stock_routers.py
│  │  ├─ multi_chat_routers.py
│  │  ├─ mystocks_routers.py
│  │  ├─ record_routers.py
│  │  ├─ set_page_routers.py
│  │  ├─ stock_routers.py
│  │  ├─ trade_routers.py
│  │  └─ __init__.py
│  ├─ services
│  │  ├─ auth_service.py
│  │  ├─ chatting_service.py
│  │  ├─ crawler_service.py
│  │  ├─ GPT_service.py
│  │  ├─ redis_service.py
│  │  ├─ stock_service.py
│  │  ├─ trade_service.py
│  │  └─ __init__.py
│  └─ __init__.py
│
│
├─ front-react
│  ├─ .prettierrc
│  ├─ package.json
│  ├─ public
│  │  ├─ favicon.ico
│  │  ├─ index.html
│  │  ├─ logo192.png
│  │  ├─ logo512.png
│  │  ├─ manifest.json
│  │  ├─ next-button.png
│  │  └─ robots.txt
│  │
│  ├─ src
│  │  ├─ App.css
│  │  ├─ App.js
│  │  ├─ App.test.js
│  │  ├─ components
│  │  │  ├─ GameStart.jsx
│  │  │  ├─ InGame.jsx
│  │  │  ├─ LoginBox.jsx
│  │  │  ├─ Navbar.jsx
│  │  │  ├─ PageSlider.jsx
│  │  │  └─ RankSlider.jsx
│  │  ├─ index.css
│  │  ├─ index.js
│  │  ├─ logo.svg
│  │  ├─ reportWebVitals.js
│  │  ├─ services
│  │  │  ├─ authservice.js
│  │  │  ├─ ChatService.js
│  │  │  └─ NewsService.js
│  │  ├─ setupTests.js
│  │  ├─ styles
│  │  │  ├─ GameStart.css
│  │  │  ├─ LoginBox.css
│  │  │  ├─ Navbar.css
│  │  │  ├─ PageSlider.css
│  │  │  └─ RankSlider.css
│  │  └─ utils
│  │     └─ api.js
│  └─ yarn.lock
│  │        
│  │        
│  └─ index.html
├─ main.py
├─ README.md
└─ requirements.txt
```
---

## 구현 기능
- 웹 크롤링 및 OpenAI API를 이용한 뉴스 게시판
- 웹소켓을 활용한 익명 유저 채팅방
- 수익률 기반 유저 랭킹을 보여주는 명예의 전당 
- 주식 매도 매수 시스템
- 종목 가격 시각화 (그래프)
- 자신의 가상 머니를 이용해 자신만의 주식을 만들어 상장시킬 수 있는 나만의 주식 상장 시스템

---

## 🚀 주요 기능
- JWT 기반의 사용자 인증 및 관리
- 실시간 모의 주식 거래 및 차트 조회
- MySQL을 활용한 안정적인 데이터 관리
- Redis 캐싱을 통한 성능 최적화
- RESTful API를 통한 프론트-백엔드 통신

---

## 🧑‍💻 팀원
- 하승원 (FRONTEND & BACKEND)
- 김민찬 (BACKEND)
- 김혜빈 (FRONTEND)
- 류아영 (UX/UI DESIGNER) #2025-03-12

## ✨ 설치 및 실행방법

**Frontend:**
```
cd ./front-react
yarn install
yarn start
```

**Backend:**
```
cd ./hambookstocks.v2
pip install -r requirements.txt
fastapi dev main.py
```

---

## 📌 현재 진행 사항
- LOGO DESIGN 및 웹 컴포넌트 구조 디자인 시작
- 주식 거래 로직 및 게임 기능 설계
- 사용자 맞춤형 기능 강화




| 이름   | 분야       | 구현 내용        | 진행 상태     | 시작 날짜  | 업데이트 시간 | 응원 메시지 |
|--------|------------|------------------|---------------|------------|---------------|-------------|
| 홍길동 | 프론트엔드 | MyPage html 구축 | HTML CSS 공부 중 | 2020.01.01 | 2022.05.05    |             |
| 김민찬 | 백엔드     | 매도/매수 요청   | 구현 중       | 2025-03-12 | 2025-03-16    |             |
| 김혜빈 | 프론트엔드 | MyPage 구현      | 구현 중       | 2025-03-12 | 2025-03-12    |             |
| 하승원 | 백엔드     | 매도/매수 요청   | 구현 중       | 2025-03-12 | 2025-03-16    |             |





## 📌진행 완료 테이블
| 구분 (프론트엔드/백엔드) | 구현 내용 (가능한 자세히 기록) | 시작 날짜 | 완료 날짜 |
|-----------------------|---------------------------|------------|------------|
| 프론트엔드 | 리액트 기반 웹 구조 세팅 (디자인 변경 필요) | 2025.02.20 | 2025.02.20 |
| 백엔드 | REDIS 도입 후 JWT 토큰 처리 | 2025.02.22 | 2025.02.22 |
| 백엔드 | SQLite에서 MySQL 데이터베이스로 전환 | 2025.02.22 | 2025.02.22 |
| 백엔드 | 기존 회원가입, 로그인, 로그아웃 로직 수정 | 2025.02.22 | 2025.02.22 |
| 백엔드 | 매일경제 최신 기사 크롤링 기능 | 2025.02.24 | 2025.02.24 |
| 백엔드 | OpenAI API를 사용하여 크롤링 기사 요약 후 반환 | 2025.02.25 | 2025.02.25 |
| 백엔드 | 요약된 기사 반환하는 API 구현 | 2025.02.25 | 2025.02.25 |
| 백엔드 | 첫 화면 전체 채팅 기능 구현 | 2025.02.25 | 2025.03.02 |
| 백엔드 | 매도/매수 시 가격 변동 기능 구현 | 2025.03.03 | 2025.03.03 |
| 프론트엔드 | 회원가입 버튼 구현 | 2025.03.06 | 2025.03.06 |
| 프론트엔드 | 로그인 기능 구현 | 2025.03.08 | 2025.03.08 |
| 프론트엔드 | 회원가입 기능 구현 | 2025.03.08 | 2025.03.08 |
| 프론트엔드 | 뉴스 화면 띄우기 | 2025.03.09 | 2025.03.09 |
| 프론트엔드 | 채팅 화면 띄우기 | 2025.03.09 | 2025.03.09 |
| 백엔드 | MyPage 기능 구현 | 2025.03.09 | 2025.03.11 |

---

© | HAMBOOK STOCKS

