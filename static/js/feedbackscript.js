document.addEventListener('DOMContentLoaded', function() {
    // Function to handle star rating
    function handleStarRating(ratingContainer) {
        const allStar = ratingContainer.querySelectorAll('.star');
        const ratingValue = ratingContainer.querySelector('input');

        // Event listener for star clicks
        allStar.forEach((star, idx) => {
            star.addEventListener('click', function() {
                // Set rating value
                ratingValue.value = idx + 1;

                // Reset all stars
                allStar.forEach(s => {
                    s.classList.replace('bxs-star', 'bx-star');
                    s.classList.remove('active');
                });

                // Highlight selected stars
                for (let i = 0; i <= idx; i++) {
                    allStar[i].classList.replace('bx-star', 'bxs-star');
                    allStar[i].classList.add('active');
                }

                // Hide required message if present
                const requiredMessage = ratingContainer.querySelector('.required-message');
                if (requiredMessage) {
                    requiredMessage.style.display = 'none';
                }

                // Reset star color
                allStar.forEach(s => {
                    s.style.color = '';
                });
            });
        });
    }

    // Selecting elements
    const submitBtns = document.querySelectorAll('.submit');
    const cancelButtons = document.querySelectorAll('.cancel');

    // Event listener for form submission
    submitBtns.forEach(submitBtn => {
        submitBtn.addEventListener('click', function(event) {
            const form = event.target.closest('form');
            const ratingContainer = form.querySelector('.rating');

            // Check if rating is required and if a rating is selected
            if (ratingContainer && !form.querySelector('.rating .star.active')) {
                const allStar = ratingContainer.querySelectorAll('.star');

                // Show required message and make stars red
                const requiredMessage = ratingContainer.querySelector('.required-message');
                if (requiredMessage) {
                    requiredMessage.style.display = 'block';
                }
                allStar.forEach(s => {
                    s.style.color = 'red';
                });

                event.preventDefault(); // Prevent form submission
            }
        });
    });

    // Event listener for cancel button
    cancelButtons.forEach(cancelButton => {
        cancelButton.addEventListener('click', function() {
            window.location.href = "/dashboard"; // Redirect to dashboard page
        });
    });

    // Event listener for star rating on forms
    const ratingContainers = document.querySelectorAll('.rating');
    ratingContainers.forEach(handleStarRating);

    // Event listener for form submission using fetch API
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            // Send form data to server
            fetch(form.action, {
                method: 'POST',
                body: new FormData(form)
            })
            .then(response => response.json())
            .then(data => {
                // Show success message and redirect
                Swal.fire({
                    icon: 'success',
                    title: data.message,
                }).then(() => {
                    window.location.href = "/dashboard";
                });
            })
            .catch(error => {
                console.error('Error:', error);
                // Show error message
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Error submitting. Please try again.',
                });
            });
        });
    });
});
