import '../styles/InGame.css';
import { buy_request, sell_request, get_my_balance } from '../services/InGameService';
import { useState, useEffect, useRef } from 'react'; // useState 추가 필요
import { connectStockWebSocket, closeWebSocket } from '../services/stock_websocket';

export default function InGame() {
  const [balance, setBalance] = useState([]);
  const [stockName, setStockName] = useState(''); // 주식 이름
  const [quantity, setQuantity] = useState(1); // 수량
  const [price, setPrice] = useState(0); // 가격
  const [stockInfo, setStockInfo] = useState([]);

  useEffect(() => {
    connectStockWebSocket(setStockInfo);

    return () => {
      closeWebSocket();
    };
  }, []);

  useEffect(() => {
    const GetBalance = async () => {
      try {
        const balanceData = await get_my_balance();
        setBalance(balanceData.balance);
      } catch (error) {
        console.error('잔액 조회 실패', error);
      }
    };
    GetBalance();
  }, []);

  const handleBuy = async () => {
    const formattedPrice = parseFloat(price);
    console.log('📌 매수 요청 데이터:', { stockName, quantity, formattedPrice });

    if (!stockName || isNaN(formattedPrice) || quantity <= 0) {
      console.error('❌ 잘못된 매수 요청 데이터!');
      return;
    }
    try {
      const response = await buy_request(stockName, price, quantity);
      console.log(response);
    } catch (error) {
      console.error('매수 실패', error);
    }
  };

  const handleSell = async () => {
    try {
      const response = await sell_request(stockName, quantity, price);
      console.log(response);
    } catch (error) {
      console.error('매도 실패', error);
    }
  };

  const handleStockClick = (selectedStockName, selectedStockPrice) => {
    setStockName(selectedStockName);
    setPrice(selectedStockPrice);
    console.log(selectedStockName, selectedStockPrice);
  };

  const handleQuantityChange = (e) => {
    const newQuantity = Number(e.target.value);
    setQuantity(newQuantity);
  };

  const totalPrice = price * quantity;

  return (
    <div className="in-game-container">
      <div className="first-section">
        <div className="stock-info">
          {/* 주식 종목 정보 */}
          <h2>주식 정보</h2>
          <div className="stock-info-item">
            <span>주식 이름</span>
            <span>주식 가격</span>
            <span>주식 레벨</span>
            <span>주식 설명</span>
          </div>

          {Object.entries(stockInfo).map(([stockName, stockPrice]) => (
            <div
              key={stockName}
              className="stock-info-item"
              onClick={() => handleStockClick(stockName, stockPrice)}
            >
              <span>{stockName}</span>
              <span>{stockPrice}</span>
              <span></span>
              <span></span>
            </div>
          ))}
        </div>
      </div>
      <div className="second-section">
        <div className="stock-chart">
          {' '}
          {/* 주식 차트 */}
          <h2>주식 차트</h2>
        </div>
        <div className="stock-trade-info">
          {' '}
          {/* 주식 거래 정보 */}
          <h2>주식 거래 정보</h2>
          <div className="stock-trade-info-item">
            <span>주식 이름</span>
            <span>주식 가격</span>
            <span>주식 수량</span>
            <span>매도 / 매수</span>
          </div>
          <div className="trade-system">
            <div className="my-balance">
              <span>나의 자산 :</span>
              <span>{balance.toLocaleString()} 원</span>
            </div>
            <div className="trade-input">
              <input
                type="number"
                placeholder="수량"
                value={quantity}
                onChange={handleQuantityChange}
                min="1"
              />
              <div className="total-price">
                <span>총 금액 :</span>
                <span>{totalPrice.toLocaleString()} 원</span>
              </div>
            </div>
            <div className="trade-button">
              <button className="buy-button" onClick={handleBuy}>
                매수
              </button>
              <button className="sell-button" onClick={handleSell}>
                매도
              </button>
            </div>
          </div>
        </div>
      </div>
      <div className="third-section">
        <div className="my-stock-info">
          {' '}
          {/* 내 주식 정보 */}
          <h2>내 주식 정보</h2>
          <div className="my-stock-info-item">
            <span>주식 이름</span>
            <span>주식 수량</span>
          </div>
        </div>
      </div>
    </div>
  );
}

// stock_id: int;
// stock_name: str;
// stock_price: float;
// stock_level: int;
// stock_description: str;
