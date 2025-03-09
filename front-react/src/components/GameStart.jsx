import '../styles/GameStart.css';
import RankSlider from './RankSlider';
import { get_news } from '../services/NewsService';
import { useState, useEffect } from 'react'; // useState 추가 필요
import { chatService } from '../services/ChatService';

export default function GameStart() {
  const dummyRankings = [
    //일단 임시데이터임
    { name: '하승원', balance: 1000000 },
    { name: '김민찬', balance: 8500 },
    { name: '이서진', balance: 7200 },
    { name: '김혜빈', balance: 6800 },
  ];

  const [news, setNews] = useState([]);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');

  useEffect(() => {
    chatService.connect();

    chatService.ws.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };

    return () => {
      chatService.disconnect();
    };
  }, []);

  // 메시지 전송 함수
  const sendMessage = () => {
    if (inputMessage.trim()) {
      chatService.sendMessage(inputMessage);
      setInputMessage('');
    }
  };

  useEffect(() => {
    const getNews = async () => {
      try {
        const newsData = await get_news();
        setNews(newsData.summarized_news);
      } catch (error) {
        console.error('뉴스 가져오기 실패', error);
      }
    };
    getNews();
  }, []); //이렇게 하면 처음 마운트 될 때만 실행됨

  return (
    <div className="game-start-container">
      {/* 뉴스 영역 */}
      <div className="top-section">
        <div className="news-section">
          {news.slice(0, 5).map((newsItem, index) => (
            <div key={index} className="news-item">
              <h3>{newsItem.제목}</h3>
              <img src={newsItem.이미지} alt={newsItem.제목} />
              <p>{newsItem.본문}</p>
              <a href={newsItem.링크} target="_blank" rel="noopener noreferrer">
                자세히 보기
              </a>
            </div>
          ))}
        </div>
        {/* 채팅 영역 */}
        <div className="chat-section">
          <h2>💬 채팅방</h2>
          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div key={index} className="chat-message">
                {typeof msg === 'string' ? msg : msg.content}
              </div>
            ))}
          </div>
          <div className="chat-input">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="메시지를 입력하세요"
            />
            <button onClick={sendMessage}>전송</button>
          </div>
        </div>
      </div>
      {/* 명예의 전당 슬라이드 영역 */}
      <RankSlider rankings={dummyRankings} />
    </div>
  );
}
