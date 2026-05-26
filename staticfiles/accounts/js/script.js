// Theme toggle
const toggle = document.getElementById('themeToggle');

if (toggle) {
    toggle.addEventListener('click', () => {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

        if (isDark) {
            document.documentElement.removeAttribute('data-theme');
        } else {
            document.documentElement.setAttribute('data-theme', 'dark');
        }
    });
}

// Auto scroll
const grid = document.getElementById('scrollGrid');
let index = 0;

function nextSlide() {
    index++;
    if (index >= 4) index = 0;

    if (grid) {
        grid.style.transform = `translateY(-${index * 220}px)`;
    }
}

setInterval(nextSlide, 3000);

