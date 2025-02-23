import { useState } from 'react';
import { CSSTransition, SwitchTransition } from 'react-transition-group';
import GameStart from './GameStart';
import InGame from './InGame';
import '../styles/PageSlider.css';

export default function PageSlider() {
  const [index, setIndex] = useState(0);

  const pages = [<GameStart />, <InGame />];

  const nextPage = () => {
    setIndex((prev) => (prev + 1) % pages.length);
  };

  return (
    <div className="page-slider-container">
      <div className="page-container">
        <SwitchTransition>
          <CSSTransition key={index} timeout={500} classNames="fade">
            <div className="page-wrapper">{pages[index]}</div>
          </CSSTransition>
        </SwitchTransition>
      </div>

      {/* 버튼을 아예 별도로 빼서 아래에 위치 */}
      <button className="next-button" onClick={nextPage}>
        <img src="/next-button.png" alt="다음 화면" />
      </button>
    </div>
  );
}
