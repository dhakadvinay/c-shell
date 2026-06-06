const filterContainer = document.getElementById('filter-container');
const projectCards = document.querySelectorAll('.project-card');


filterContainer.addEventListener('click', (event) => {
    

    if (event.target.classList.contains('filter-btn')) {
        
        const clickedTag = event.target.getAttribute('data-tech');
        const myUrl = new URL(window.location);
        if (clickedTag === 'clear') {
            myUrl.searchParams.delete('filter'); 
        } else {
            myUrl.searchParams.set('filter', clickedTag); 
        }
        window.history.replaceState({}, '', myUrl);

        for (let card of projectCards) {
            const cardTags = card.getAttribute('data-tags');
            
            if (clickedTag === 'clear') {
                card.style.display = 'block';
            } else if (cardTags.includes(clickedTag)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        }
    }
});


const loadParams = new URLSearchParams(window.location.search);
const savedFilter = loadParams.get('filter');

if (savedFilter !== null) {
    const buttonToClick = document.querySelector(`.filter-btn[data-tech="${savedFilter}"]`);
    if (buttonToClick) {
        buttonToClick.click();
    }
}