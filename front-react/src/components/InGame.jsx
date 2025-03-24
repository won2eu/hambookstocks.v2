import '../styles/InGame.css';
import React, { useEffect, useState } from 'react';
import { getMyStocks } from '../services/InGame';

export default function InGame() {
  const [mystocks, setMystocks] = useState([]);  // 보유 주식 정보 상태
  const [error, setError] = useState(null);  // 에러 상태

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

  return (
    <div className="in-game-container">
      <div className="first-section">
        <div className="stock-info">
          {' '}
          {/* 주식 종목 정보 */}
          <h2>주식 정보</h2>
          <div className="stock-info-item">
            <span>주식 이름</span>
            <span>주식 가격</span>
            <span>주식 레벨</span>
            <span>주식 설명</span>
          </div>
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
              <span>1000000</span>
            </div>
            <div className="trade-input">
              <input type="number" placeholder="수량" />
              <div className="total-price">
                <span>총 금액 :</span>
              </div>
            </div>
            <div className="trade-button">
              <button className="buy-button">매수</button>
              <button className="sell-button">매도</button>
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
