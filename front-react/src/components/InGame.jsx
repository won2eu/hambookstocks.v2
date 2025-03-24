import '../styles/InGame.css';
import { buy_request, sell_request, get_my_balance } from '../services/InGameService';
import React, { useState, useEffect, useRef } from 'react'; // useState 추가 필요
import { connectStockWebSocket, closeWebSocket } from '../services/stock_websocket';
import { get_stock_detail, get_trade_stocks } from '../services/InGameService';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { getMyStocks } from '../services/InGame';

export default function InGame() {
  const [mystocks, setMystocks] = useState([]);  // 보유 주식 정보 상태
  const [error, setError] = useState(null);  // 에러 상태
  const [balance, setBalance] = useState([]);
  const [stockName, setStockName] = useState(''); // 주식 이름
  const [quantity, setQuantity] = useState(1); // 수량
  const [price, setPrice] = useState(0); // 가격
  const [stockInfo, setStockInfo] = useState([]);
  const [stockHistory, setStockHistory] = useState([]);
  const [tradeQuantity, setTradeQuantity] = useState(0);
  const [isBuy, setIsBuy] = useState(true);
  const [isStockSelected, setIsStockSelected] = useState(false); // 주식이 선택되었는지 여부
  const [stockDetail, setStockDetail] = useState([]);

  useEffect(() => {
    const fetchStocks = async () => {
      try {
        const stocks = await getMyStocks();
        /*console.log("📊 가져온 주식 데이터:", stocks); // 가져온 데이터를 확인*/
        setMystocks(stocks);  // mystocks 상태 업데이트
        /*console.log("📊 mystocks 상태값:", stocks); // 상태 확인*/
      } catch (err) {
        console.error("❌ API 에러:", err.message);
        setError("주식 정보를 가져오는 데 실패했습니다.");  // 에러 메시지 설정
      }
    };
  
    fetchStocks();  // 컴포넌트 렌더링 시 호출
  }, []);

  useEffect(() => {
    connectStockWebSocket(setStockInfo);

    return () => {
      closeWebSocket();
    };
  }, []);

  useEffect(() => {
    setStockHistory([]); // ✅ 종목 변경 시 기존 데이터 초기화
  }, [stockName]); // stockName이 바뀔 때마다 실행

  useEffect(() => {
    if (stockName && stockInfo[stockName]) {
      // stockName에 해당하는 데이터만 추가
      const now = new Date();
      const time = `${now.getHours()}:${now.getMinutes()}:${now.getSeconds()}`;

      setStockHistory((prevHistory) => [
        ...prevHistory.slice(-30), // 최근 30개 데이터만 유지
        { time, price: stockInfo[stockName] },
      ]);
    }
  }, [stockName, stockInfo]);

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
      const response = await buy_request(stockName, quantity, price);
      console.log(response);
    } catch (error) {
      console.error('매수 실패', error);
    }
  };

  const handleSell = async () => {
    try {
      const response = await sell_request(stockName, quantity, quantity);
      console.log(response);
    } catch (error) {
      console.error('매도 실패', error);
    }
  };

  const handleStockDetail = async (stockName) => {
    try {
      const detail = await get_stock_detail(stockName);
      setStockDetail(detail);
    } catch (error) {
      console.error('주식 상세 조회 실패', error);
    }
  };

  const handleStockClick = async (selectedStockName, selectedStockPrice) => {
    if (stockName === selectedStockName && isStockSelected) {
      setIsStockSelected(false);
      return;
    }
    setIsStockSelected(false);
    setStockName(selectedStockName);
    setPrice(selectedStockPrice);

    try {
      const trade_stocks = await get_trade_stocks(selectedStockName);
      setTradeQuantity(trade_stocks.stock_quantity); //주식 상장하면 tradestocks에 올려야됨
      setIsBuy(trade_stocks.is_buy);

      await handleStockDetail(selectedStockName);

      setTimeout(() => {
        setIsStockSelected(true);
      }, 100);
    } catch (error) {
      console.error('주식 매도/매수 조회 실패', error);
    }
  };

  const handleQuantityChange = (e) => {
    const newQuantity = Number(e.target.value);
    setQuantity(newQuantity);
    console.log('입력된 수량:', newQuantity);
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
          </div>

          {Object.entries(stockInfo).map(([stockName, stockPrice]) => (
            <div
              key={stockName}
              className="stock-info-item"
              onClick={async () => await handleStockClick(stockName, stockPrice)}
            >
              <span className="stock-name">{stockName}</span>
              <span>{stockPrice}</span>
            </div>
          ))}
        </div>
        <div className={`stock-detail ${isStockSelected ? 'show' : ''}`}>
          {stockDetail && (
            <>
              <h3>{stockName}</h3>
              <div className="stock-info-container">
                <span className="label">주식 레벨 :</span>
                <span className="value">{stockDetail.stock_level}</span>

                <span className="label">주식 설명 :</span>
                <span className="value">{stockDetail.stock_description}</span>
              </div>
            </>
          )}
        </div>
      </div>
      <div className="second-section">
        <div className="stock-chart">
          {' '}
          {/* 주식 차트 */}
          <h2>주식 차트</h2>
          {stockHistory.length > 0 ? (
            <div className="chart-container">
              <LineChart width={800} height={400} data={stockHistory}>
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <CartesianGrid stroke="#ccc" />
                <Line type="monotone" dataKey="price" stroke="#8884d8" />
              </LineChart>
            </div>
          ) : (
            <p>주식 종목을 클릭하여 차트를 확인해보세요.</p>
          )}
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
          <div className="stock-trade-info-item">
            <span>{stockName}</span>
            <span>{price}</span>
            <span>{tradeQuantity}</span>
            <span>{isBuy ? '매수' : '매도'}</span>
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
          {/* 내 보유 주식 정보 렌더링 */}
          {mystocks.length > 0 ? (
            mystocks.map((stock) => (
              <div key={stock.id} className="my-stock-item">
                <span>{stock.stock_name}</span>
                <span>{stock.quantity}</span> {/* 주식 수량 */}
              </div>
            ))
          ) : (
            <div>주식 정보가 없습니다.</div>
          )}
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
