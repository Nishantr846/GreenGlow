document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.querySelector('.search-input');

    if (!searchInput) {
        console.error('Search input element not found');
        return;
    }

    // Get all cards (either articles or div.card)
    let items = document.querySelectorAll('article, .card');

    function searchItems() {
        const query = searchInput.value.toLowerCase();
        items.forEach(item => {
            const titleElement = item.querySelector('h2');
            const descriptionElement = item.querySelector('p');

            const title = titleElement ? titleElement.textContent.toLowerCase() : '';
            const description = descriptionElement ? descriptionElement.textContent.toLowerCase() : '';

            if (title.includes(query) || description.includes(query)) {
                item.style.display = 'block'; // Show matching
            } else {
                item.style.display = 'none'; // Hide non-matching
            }
        });
    }

    searchInput.addEventListener('input', searchItems);
});


document.addEventListener("DOMContentLoaded", function () {
    const detectBtn = document.querySelector('.detect-btn');
    const fileInput = document.getElementById('file-upload');

    detectBtn.addEventListener('click', async () => {
        const file = fileInput.files[0];
        if (!file) {
            alert("Please select an image.");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            alert("Predicted Disease: " + data.prediction);
        } catch (error) {
            console.error(error);
            alert("Error during prediction.");
        }
    });
});




// Function to handle the file upload and prediction request

async function predictDisease() {
    const fileInput = document.getElementById('file-upload');
    const resultText = document.getElementById('prediction-result');

    if (!fileInput.files[0]) {
        resultText.textContent = "Please upload an image first.";
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            body: formData
        });
        // Replace http://localhost:5000 with your actual hosted Flask backend URL once deployed (e.g., https://yourapp.onrender.com)

        if (!response.ok) {
            throw new Error("Prediction failed");
        }

        const data = await response.json();
        resultText.textContent = "Predicted Disease: " + data.disease;
    } catch (error) {
        resultText.textContent = "Error: " + error.message;
    }
}

