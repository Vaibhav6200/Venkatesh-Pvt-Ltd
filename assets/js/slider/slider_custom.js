var service_swiper = new Swiper(".mySwiper", {
    slidesPerView: 3,
    centreSlides: true,
    spaceBetween: 30,
    dragCursor: true,
    loop: true,
    pagination: {
        el: ".swiper-pagination",
        autoScroll: true,
        dynamicBullets: true
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    autoplay: {
        delay: 2500,
        disableOnInteraction: false,
    },
    breakpoints: {
        0:{
            slidesPerView: 1,
        },
        576:{
            slidesPerView: 2,
        },
        992:{
            slidesPerView: 3,
        }
    }
});



var deals_and_discount_swiper = new Swiper(".deals_and_discount_swiper", {
    spaceBetween: 30,
    loop: true,
    pagination: {
      el: ".swiper-pagination",
      dynamicBullets: true,
      autoScroll: true,
      clickable: true,
    },
    autoplay: {
        delay: 2500,
        disableOnInteraction: false,
    },
});