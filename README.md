# HambookStocks

[고쳐야 하는 내용] :

[수정 사항] :
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
├─ front
│  ├─ assets
│  │  ├─ css
│  │  │  ├─ owl.css
│  │  │  ├─ styles.css
│  │  │  └─ templatemo-grad-school.css
│  │  ├─ fonts
│  │  │  ├─ Flaticon.woff
│  │  │  ├─ flexslider-icon.eot
│  │  │  ├─ flexslider-icon.svg
│  │  │  ├─ flexslider-icon.ttf
│  │  │  ├─ flexslider-icon.woff
│  │  │  ├─ fontawesome-webfont.eot
│  │  │  ├─ fontawesome-webfont.svg
│  │  │  ├─ fontawesome-webfont.ttf
│  │  │  ├─ fontawesome-webfont.woff
│  │  │  ├─ fontawesome-webfont.woff2
│  │  │  ├─ FontAwesome.otf
│  │  │  ├─ slick.eot
│  │  │  ├─ slick.svg
│  │  │  ├─ slick.ttf
│  │  │  └─ slick.woff
│  │  └─ js
│  │     ├─ custom.js
│  │     ├─ owl-carousel.js
│  │     ├─ server.js
│  │     ├─ signup.js
│  │     ├─ slick-slider.js
│  │     └─ video.js
│  ├─ index.html
│  ├─ prepros-6.config
│  ├─ prepros.config
│  ├─ signup.html
│  └─ vendor
│     ├─ bootstrap
│     │  ├─ css
│     │  │  └─ bootstrap.min.css
│     │  └─ js
│     │     └─ bootstrap.min.js
│     └─ jquery
│        ├─ jquery.js
│        ├─ jquery.min.js
│        ├─ jquery.min.map
│        ├─ jquery.slim.js
│        ├─ jquery.slim.min.js
│        └─ jquery.slim.min.map
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
├─ front2
│  ├─ assets
│  │  ├─ css
│  │  │  ├─ bootstrap.css
│  │  │  ├─ bootstrap.min.css
│  │  │  ├─ demo.css
│  │  │  ├─ demo.css.map
│  │  │  ├─ main.css
│  │  │  └─ main.css.map
│  │  ├─ img
│  │  │  └─ 임시사진.jpg
│  │  ├─ scripts
│  │  │  └─ klorofil-common.js
│  │  └─ vendor
│  │     ├─ bootstrap
│  │     │  ├─ css
│  │     │  │  ├─ bootstrap-theme.css
│  │     │  │  ├─ bootstrap-theme.min.css
│  │     │  │  ├─ bootstrap.css
│  │     │  │  └─ bootstrap.min.css
│  │     │  ├─ fonts
│  │     │  │  ├─ glyphicons-halflings-regular.eot
│  │     │  │  ├─ glyphicons-halflings-regular.svg
│  │     │  │  ├─ glyphicons-halflings-regular.ttf
│  │     │  │  ├─ glyphicons-halflings-regular.woff
│  │     │  │  └─ glyphicons-halflings-regular.woff2
│  │     │  └─ js
│  │     │     ├─ bootstrap.js
│  │     │     ├─ bootstrap.min.js
│  │     │     └─ npm.js
│  │     ├─ chartist
│  │     │  ├─ css
│  │     │  │  ├─ chartist-custom.css
│  │     │  │  ├─ chartist-custom.css.map
│  │     │  │  ├─ chartist.css
│  │     │  │  └─ chartist.min.css
│  │     │  ├─ js
│  │     │  │  ├─ chartist.js
│  │     │  │  └─ chartist.min.js
│  │     │  ├─ map
│  │     │  │  ├─ chartist.css.map
│  │     │  │  └─ chartist.min.js.map
│  │     │  └─ scss
│  │     │     └─ chartist.scss
│  │     ├─ font-awesome
│  │     │  ├─ css
│  │     │  │  ├─ font-awesome.css
│  │     │  │  └─ font-awesome.min.css
│  │     │  └─ fonts
│  │     │     ├─ fontawesome-webfont.eot
│  │     │     ├─ fontawesome-webfont.svg
│  │     │     ├─ fontawesome-webfont.ttf
│  │     │     ├─ fontawesome-webfont.woff
│  │     │     ├─ fontawesome-webfont.woff2
│  │     │     └─ FontAwesome.otf
│  │     ├─ jquery
│  │     │  ├─ jquery.js
│  │     │  ├─ jquery.min.js
│  │     │  └─ jquery.min.map
│  │     ├─ jquery-slimscroll
│  │     │  ├─ jquery.slimscroll.js
│  │     │  └─ jquery.slimscroll.min.js
│  │     ├─ jquery.easy-pie-chart
│  │     │  ├─ angular.easypiechart.js
│  │     │  ├─ angular.easypiechart.min.js
│  │     │  ├─ easypiechart.js
│  │     │  ├─ easypiechart.min.js
│  │     │  ├─ jquery.easypiechart.js
│  │     │  └─ jquery.easypiechart.min.js
│  │     ├─ linearicons
│  │     │  ├─ fonts
│  │     │  │  ├─ Linearicons-Free.eot
│  │     │  │  ├─ Linearicons-Free.svg
│  │     │  │  ├─ Linearicons-Free.ttf
│  │     │  │  ├─ Linearicons-Free.woff
│  │     │  │  └─ Linearicons-Free.woff2
│  │     │  └─ style.css
│  │     └─ toastr
│  │        ├─ toastr.css
│  │        ├─ toastr.js
│  │        ├─ toastr.min.css
│  │        └─ toastr.min.js
│  └─ index.html
├─ main.py
├─ README.md
├─ requirements.txt
└─ 코드_종목명_0206.csv

```