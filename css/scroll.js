function scrollCards(direction) {
    const wrapper = document.getElementById('cardWrapper');
    const cardWidth = wrapper.offsetWidth;
    const currentScroll = wrapper.scrollLeft;
    
    if (direction === 'next') {
        wrapper.scrollTo({
            left: currentScroll + cardWidth,
            behavior: 'smooth'
        });
    } else {
        wrapper.scrollTo({
            left: currentScroll - cardWidth,
            behavior: 'smooth'
        });
    }
}

// Add keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') {
        scrollCards('next');
    } else if (e.key === 'ArrowLeft') {
        scrollCards('prev');
    }
});