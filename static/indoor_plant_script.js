// Select all the article cards
const cards = document.querySelectorAll('.article-card');

// Loop through each card and add an event listener for clicks
cards.forEach(card => {
    card.addEventListener('click', () => {
        // Toggle the 'clicked' class to show/hide the effect
        card.classList.toggle('clicked');
    });
});