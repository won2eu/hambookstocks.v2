import { Swiper, SwiperSlide } from 'swiper/react';
import { EffectCoverflow, Pagination, Autoplay } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/effect-coverflow';
import 'swiper/css/pagination';
import '../styles/RankSlider.css';

export default function RankSlider({ rankings }) {
  return (
    <div className="rank-slider-section">
      <Swiper
        effect={'coverflow'}
        grabCursor={true}
        centeredSlides={true}
        slidesPerView={3}
        loop={true}
        autoplay={{
          delay: 1500,
          disableOnInteraction: false,
        }}
        coverflowEffect={{
          rotate: 50,
          stretch: 0,
          depth: 100,
          modifier: 1,
          slideShadows: false,
        }}
        pagination={true}
        spaceBetween={210}
        modules={[EffectCoverflow, Pagination, Autoplay]}
      >
        {rankings.map((rank, index) => (
          <SwiperSlide key={index}>
            <div className="rank-card">
              <h3>[{index + 1}등]</h3>
              <p>{rank.name}</p>
              <p>{rank.balance}원</p>
            </div>
          </SwiperSlide>
        ))}
      </Swiper>
    </div>
  );
}
