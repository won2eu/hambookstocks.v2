class WebSocketService {
    constructor() {
      this.ws = null;
    }
  
    connect() {
      const token = localStorage.getItem('token');
      const guestId = token ? null : 'guest_' + Math.random().toString(36).substring(2, 9);
      
      // 기본 연결
      this.ws = new WebSocket('ws://localhost:8000/multichat/ws');
      // 연결 성공 시 인증 데이터 전송
      console.log(this.ws);
      this.ws.onopen = () => {
        // 첫 메시지로 인증 데이터 전송
        const authData = {
            type: 'auth'  // 인증 메시지임을 표시
          };
          // token이 있을 때만 authorization 추가
          if (token) {
            authData.authorization = `Bearer ${token}`;
          }
          // guestId가 있을 때만 guest_id 추가
          if (guestId) {
            authData.guest_id = guestId;
          }
        this.ws.send(JSON.stringify(authData));
      };

      // 메시지 수신
      this.ws.onmessage = (event) => {
        console.log('받은 메시지:', event.data);
      };

      // 에러 처리
      this.ws.onerror = (error) => {
        console.error('WebSocket 에러:', error);
      };
    }
  
    sendMessage(message) {
      if (this.ws) {
        // 일반 채팅 메시지
        const chatData = {
          type: 'message',
          content: message
        };
        this.ws.send(JSON.stringify(chatData));
      }
    }
  
    disconnect() {
      if (this.ws) {
        this.ws.close();
      }
    }
}
  
export const chatService = new WebSocketService();