
const timelineList = document.getElementById('timeline-list');

timelineList.addEventListener('click', (event) => {
    if (event.target.classList.contains('timeline-btn')) {
        
        const clickedBtn = event.target;
        const contentDiv = clickedBtn.nextElementSibling;
        const isExpanded = clickedBtn.getAttribute('aria-expanded');
        
        if (isExpanded === 'false') {
            clickedBtn.setAttribute('aria-expanded', 'true');
            contentDiv.classList.add('show');
        } else {
            clickedBtn.setAttribute('aria-expanded', 'false');
            contentDiv.classList.remove('show');
        }
    }
});