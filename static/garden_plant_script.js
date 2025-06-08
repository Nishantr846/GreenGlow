/* FOR DROPDOWN MENU */

const plantTypeSelect = document.getElementById('plant-type-select');
const floralSection = document.getElementById('floral-plants-section');
const kitchenSection = document.getElementById('kitchen-plants-section');

plantTypeSelect.addEventListener('change', function () {
    if (this.value === 'floral') {
        floralSection.style.display = 'block';
        kitchenSection.style.display = 'none';
    } else if (this.value === 'kitchen') {
        floralSection.style.display = 'none';
        kitchenSection.style.display = 'block';
    }
});

const dropdownWrapper = document.querySelector('.dropdown-wrapper');
const selectElement = document.getElementById('plant-type-select');

selectElement.addEventListener('click', function () {
    dropdownWrapper.classList.toggle('active');
});

selectElement.addEventListener('blur', function () {
    dropdownWrapper.classList.remove('active');
});

/* FOR HOVERING OVER THE Plant cards */


document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('click', function () {
        // Add "open" class to the clicked card
        this.classList.add('open');

        // Create an overlay div
        const overlay = document.createElement('div');
        overlay.classList.add('overlay');

        // Create the close button
        const closeButton = document.createElement('button');
        closeButton.classList.add('close-btn');
        closeButton.innerHTML = '&times;'; // This is the cross symbol

        // Append the close button to the card
        this.appendChild(closeButton);

        // Append overlay to body
        document.body.appendChild(overlay);

        // Show the overlay with fade-in effect
        setTimeout(() => {
            overlay.classList.add('show');
        }, 10);

        // Add a blur effect to the body background
        document.body.classList.add('blur-background');

        // Close the card when overlay or close button is clicked
        overlay.addEventListener('click', () => {
            this.classList.remove('open');
            overlay.classList.remove('show'); // Fade-out effect
            document.body.removeChild(overlay); // Remove the overlay from DOM
            this.removeChild(closeButton); // Remove close button
            document.body.classList.remove('blur-background'); // Remove blur from background
        });

        // Close the card when the close button is clicked
        closeButton.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent the card from closing when the button is clicked
            this.classList.remove('open');
            overlay.classList.remove('show'); // Fade-out effect
            document.body.removeChild(overlay); // Remove the overlay from DOM
            this.removeChild(closeButton); // Remove close button
            document.body.classList.remove('blur-background'); // Remove blur from background
        });
    });
});
