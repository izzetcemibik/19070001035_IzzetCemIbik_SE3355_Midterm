const slider = document.querySelector('.slider');
let autoSlideTimer;

function autoSlide() {
    const slides = document.querySelectorAll('.slide');
    const currentSlide = document.querySelector('.slide.active');
    const currentIndex = Array.from(slides).indexOf(currentSlide);
    const nextIndex = (currentIndex + 1) % slides.length;
    const nextSlide = slides[nextIndex];
    
    slideTo(nextSlide);
}

function slideTo(slide) {
    const slideIndex = Array.from(slide.parentNode.children).indexOf(slide);
    const slideWidth = slide.offsetWidth;
    
    slider.style.transform = `translateX(-${slideIndex * slideWidth}px)`;
    
    document.querySelector('.slide.active').classList.remove('active');
    slide.classList.add('active');
}

autoSlideTimer = setInterval(autoSlide, 2000);

const slides = document.querySelectorAll('.slide');
slides.forEach(slide => {
    slide.addEventListener('transitionend', () => {
        clearInterval(autoSlideTimer); 
        autoSlideTimer = setInterval(autoSlide, 2000);
    });
});
