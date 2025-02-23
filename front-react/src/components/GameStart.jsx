import '../styles/GameStart.css';
import RankSlider from './RankSlider';

export default function GameStart() {
  const dummyRankings = [
    { name: '하승원', balance: 1000000 },
    { name: '김민찬', balance: 8500 },
    { name: '이서진', balance: 7200 },
    { name: '김혜빈', balance: 6800 },
  ];

  return (
    <div className="game-start-container">
      {/* 뉴스 영역 */}
      <div className="top-section">
        <div className="news-section">
          <h2>📢 오늘의 뉴스</h2>
          <p>여기에 뉴스 내용이 들어갑니다.</p>
          <p>여기에 뉴스 내용이 들어갑니다.</p>
          <p>여기에 뉴스 내용이 들어갑니다.</p>
          <p>여기에 뉴스 내용이 들어갑니다.</p>
          <p>여기에 뉴스 내용이 들어갑니다.</p>
          <p>여기에 뉴스 내용이 들어갑니다.</p>
        </div>

        {/* 채팅 영역 */}
        <div className="chat-section">
          <h2>💬 채팅방</h2>
          <p>유저들과 소통하는 공간입니다.</p>
        </div>
      </div>
      {/* 명예의 전당 슬라이드 영역 */}
      <RankSlider rankings={dummyRankings} />
    </div>
  );
}
