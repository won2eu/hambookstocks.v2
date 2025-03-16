import '../styles/GameStart.css';
import RankSlider from './RankSlider';
import { get_news } from '../services/NewsService';
import { useState, useEffect, useRef } from 'react'; // useState 추가 필요
import { chatService } from '../services/ChatService';

export default function GameStart() {
  const dummyRankings = [
    //일단 임시데이터임
    { name: '곧 출시될 예정입니다.', balance: 2025.04 },
    { name: '곧 출시될 예정입니다.', balance: 2025.04 },
    { name: '곧 출시될 예정입니다.', balance: 2025.04 },
    { name: '곧 출시될 예정입니다.', balance: 2025.04 },
  ];

  const [news, setNews] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [messages, setMessages] = useState(
    JSON.parse(sessionStorage.getItem('chatMessages')) || [],
  ); //parse는 제이슨 문자열을 자바스크립트 객체(초기 상태)로 변환하는 함수

  const chatMessagesRef = useRef(null);
  useEffect(() => {
    if (chatMessagesRef.current) {
      chatMessagesRef.current.scrollTop = chatMessagesRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    chatService.connect();

    chatService.ws.onmessage = (event) => {
      setMessages((prev) => {
        const newMessages = [...prev, event.data];
        sessionStorage.setItem('chatMessages', JSON.stringify(newMessages));
        return newMessages;
      });
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
          <h2>STOCK TALK</h2>
          <div className="chat-messages" ref={chatMessagesRef}>
            {messages.map((msg, index) => {
              try {
                // JSON 형태의 메시지 처리
                const messageObj =
                  typeof msg === 'string' ? JSON.parse(msg.split(' says: ')[1]) : msg;
                const username = msg.split(' says: ')[0].replace('Client #', '');
                const content = messageObj.content; // JSON에서 content 추출

                const loginId = localStorage.getItem('login_id');
                let currentUser = loginId || chatService.guestId;

                if (loginId && username.startsWith('guest_')) {
                  currentUser = chatService.guestId;
                }

                const isMyMessage = username === currentUser;
                return (
                  <div
                    key={index}
                    className={`chat-message ${isMyMessage ? 'my-message' : 'other-message'}`}
                  >
                    <span className="username">{username}</span>
                    <span className="separator">: </span>
                    <span className="content">{content}</span>
                  </div>
                );
              } catch (error) {
                console.log('메시지 파싱 에러:', error);
                return null;
              }
            })}
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
