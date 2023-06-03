import styled from "styled-components";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import "swiper/css/effect-cards";
import { EffectCards, Navigation, Pagination, Autoplay } from "swiper";
import Arrow from "../assets/Arrow.svg";

import img1 from "../assets/Nfts/bighead-1.svg";
import img2 from "../assets/Nfts/bighead-2.svg";
import img3 from "../assets/Nfts/bighead-3.svg";
import img4 from "../assets/Nfts/bighead-4.svg";
import img5 from "../assets/Nfts/bighead-5.svg";
import img6 from "../assets/Nfts/bighead-6.svg";
import img7 from "../assets/Nfts/bighead-7.svg";
import img8 from "../assets/Nfts/bighead-8.svg";
import img9 from "../assets/Nfts/bighead-9.svg";
import img10 from "../assets/Nfts/bighead-10.svg";
import Image from "next/image";

const Container = styled.div`
  width: 25vw;
  height: 70vh;

  .swiper {
    width: 100%;
    height: 100%;
  }

  .swiper-slide {
    background-color: ${(props) => props.theme.carouselColor};
    border-radius: 20px;

    display: flex;
    justify-content: center;
    align-items: center;
  }

  .swiper-button-next {
    color: ${(props) => props.theme.text};
    right: 0;
    top: 60%;
    width: 4rem;

    background-image: url(${Arrow});
    background-position: center;
    background-size: cover;

    &:after {
      display: none;
    }
  }

  .swiper-button-prev {
    color: ${(props) => props.theme.text};
    left: 0;
    top: 60%;
    width: 4rem;
    transform: rotate(180deg);

    background-image: url(${Arrow});
    background-position: center;
    background-size: cover;

    &:after {
      display: none;
    }
  }
`;
function Carousel() {
  return (
    <Container>
      <Swiper
        autoplay={{
          delay: 2000,
          disableOnInteraction: false,
        }}
        pagination={{
          type: "fraction",
        }}
        navigation={true}
        scrollbar={{
          draggable: true,
        }}
        effect={"cards"}
        grabCursor={true}
        modules={[EffectCards, Navigation, Pagination, Autoplay]}
        className="mySwiper"
      >
        <SwiperSlide>
          {" "}
          <Image src={img1} alt="The NAS" />{" "}
        </SwiperSlide>
        <SwiperSlide>
          {" "}
          <Image src={img2} alt="The NAS" />{" "}
        </SwiperSlide>
        <SwiperSlide>
          {" "}
          <Image src={img3} alt="The NAS" />{" "}
        </SwiperSlide>
        <SwiperSlide>
          {" "}
          <Image src={img4} alt="The NAS" />{" "}
        </SwiperSlide>
        <SwiperSlide>
          {" "}
          <Image src={img5} alt="The NAS" />{" "}
        </SwiperSlide>
        <SwiperSlide>
          {" "}
          <Image src={img6} alt="The NAS" />{" "}
        </SwiperSlide>
        <SwiperSlide>
          {" "}
          <Image src={img7} alt="The NAS" />{" "}
        </SwiperSlide>
        <SwiperSlide>
          {" "}
          <Image src={img8} alt="The NAS" />{" "}
        </SwiperSlide>
        <SwiperSlide>
          {" "}
          <Image src={img9} alt="The NAS" />{" "}
        </SwiperSlide>
        <SwiperSlide>
          {" "}
          <Image src={img10} alt="The NAS" />{" "}
        </SwiperSlide>
      </Swiper>
    </Container>
  );
}

export default Carousel;
