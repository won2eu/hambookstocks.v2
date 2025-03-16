import './App.css';
import Navbar from './components/Navbar';
import PageSlider from './components/PageSlider'
import MyPage from './components/MyPage'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

 /* function App() {
  return (
    <div className="App">
    <Navbar />
    <PageSlider />
    <MyPage />
    </div>
  );
} */

function App() {
  return (
    <Router>  {/* Router 추가 */}
      <div className="App">
        <Navbar />
        <Routes>  {/* Routes 안에 페이지 라우팅 설정 */}
          <Route path="/" element={<PageSlider />} />
          <Route path="/mypage" element={<MyPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;