// script.js

// Get elements from the DOM
const counterElement = document.querySelector('.counter');
const loadingBarFront = document.querySelector('.loading-bar-front');

// Initialize the counter
let progress = 0;

// Function to update the loading screen
function updateLoading() {
    progress += 1;
    counterElement.textContent = `${progress}%`;
    loadingBarFront.style.width = `${progress}%`;

    if (progress < 100) {
        setTimeout(updateLoading, 50); // Adjust the speed here (50ms per increment)
    } else {
        // Once loading completes, you can redirect or display something else
        setTimeout(() => {
            document.body.innerHTML = '<h1>Welcome to the App!</h1>';
        }, 500);
    }
}

// Start the loading animation
updateLoading();
