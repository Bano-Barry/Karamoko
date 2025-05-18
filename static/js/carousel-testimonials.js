document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelectorAll('#carousel-temoignages .carousel-slide');
    const dotsContainer = document.getElementById('carousel-dots');
    let current = 0;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.toggle('hidden', i !== index);
        });
        // Update dots
        Array.from(dotsContainer.children).forEach((dot, i) => {
            dot.classList.toggle('bg-orange-500', i === index);
            dot.classList.toggle('bg-gray-300', i !== index);
        });
    }

    // Create dots
    slides.forEach((_, i) => {
        const dot = document.createElement('button');
        dot.className = 'w-3 h-3 rounded-full bg-gray-300 focus:outline-none';
        dot.addEventListener('click', () => {
            current = i;
            showSlide(current);
        });
        dotsContainer.appendChild(dot);
    });

    document.getElementById('prev-slide').onclick = function () {
        current = (current - 1 + slides.length) % slides.length;
        showSlide(current);
    };
    document.getElementById('next-slide').onclick = function () {
        current = (current + 1) % slides.length;
        showSlide(current);
    };

    // Auto-slide (optionnel)
    setInterval(() => {
        current = (current + 1) % slides.length;
        showSlide(current);
    }, 5000);

    showSlide(current);
});