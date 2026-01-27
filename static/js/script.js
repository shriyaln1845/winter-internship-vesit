document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('riskForm');
    const resultContainer = document.getElementById('result-container');
    const analyzeBtn = form.querySelector('button[type="submit"]');

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Basic UI Feedback
            analyzeBtn.textContent = "Analyzing...";
            analyzeBtn.disabled = true;

            // Collect Data
            const formData = new FormData(form);
            const data = {};

            // Convert numbers
            const numberFields = ['age', 'height', 'weight', 'daily_steps', 'sleep_duration'];

            formData.forEach((value, key) => {
                if (numberFields.includes(key)) {
                    data[key] = parseFloat(value);
                } else {
                    data[key] = value;
                }
            });

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const result = await response.json();

                // Save to localStorage/sessionStorage for dashboard simulation
                sessionStorage.setItem('lastRiskResult', JSON.stringify(result));

                // Display Result
                displayResult(result);

            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while processing your request. Please try again.');
            } finally {
                analyzeBtn.textContent = "Analyze Risk";
                analyzeBtn.disabled = false;
            }
        });
    }

    function displayResult(result) {
        form.style.display = 'none';
        resultContainer.style.display = 'block';

        const scoreEl = document.getElementById('result-score');
        const badgeEl = document.getElementById('result-badge');

        scoreEl.textContent = result.risk_score + '%';
        badgeEl.textContent = result.risk_level;

        badgeEl.className = 'badge'; // clear previous classes
        if (result.risk_level === 'Low') {
            badgeEl.classList.add('bg-low');
        } else if (result.risk_level === 'Moderate') {
            badgeEl.classList.add('bg-moderate');
        } else {
            badgeEl.classList.add('bg-high');
        }

        // Scroll into view
        resultContainer.scrollIntoView({ behavior: 'smooth' });
    }
});
