let socket = null;

export const connectStockWebSocket  = (onMessage, onClose) => {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
        socket = new WebSocket("ws://15.165.205.43:8000/get_info/stock_info");

        socket.onopen = () => {
            console.log("WebSocket 연결 성공");
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            onMessage(data); // 콜백 함수 실행 (React에서 상태 업데이트)
        };

        socket.onclose = () => {
            console.log("WebSocket 연결 종료");
            if (onClose) onClose();
        };
    }
};

export const closeWebSocket = () => {
    if (socket) {
        socket.close();
        console.log("🔌 WebSocket 수동 종료");
    }
};