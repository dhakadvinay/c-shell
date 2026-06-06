
const themeBtn = document.getElementById('theme-btn');

if (themeBtn) {
    themeBtn.addEventListener('click', () => {
        const body = document.body;
        
        if (body.classList.contains('theme-light')) {
            body.className = 'theme-dark';
            localStorage.setItem('myTheme', 'theme-dark');
        } else {
            body.className = 'theme-light';
            localStorage.setItem('myTheme', 'theme-light');
        }
    });
}


const scrollElements = document.querySelectorAll('.scroll-fade');

const myObserver = new IntersectionObserver((entries) => {
    for (let entry of entries) {
        if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
        }
    }
});

for (let el of scrollElements) {
    myObserver.observe(el);
}