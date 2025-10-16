/* ================================================================
   VBIT NEWSLETTER - INTERACTIVE JAVASCRIPT
   Star Rating Functionality
   ================================================================ */

function hoverStars(rating) {
    const stars = document.querySelectorAll('.star-link');
    const label = document.getElementById('ratingLabel');
    
    const colors = {
        1: '#CC3333',  // VBIT Red
        2: '#f97316',  // Orange-Red
        3: '#F39434',  // VBIT Orange
        4: '#336699',  // VBIT Blue
        5: '#339933'   // VBIT Green
    };
    
    const labels = {
        1: 'Very Poor',
        2: 'Poor',
        3: 'Average',
        4: 'Good',
        5: 'Excellent'
    };
    
    stars.forEach((star, index) => {
        if (index < rating) {
            star.style.color = colors[rating];
            star.style.transform = 'scale(1.2)';
        } else {
            star.style.color = '#d1d5db';
            star.style.transform = 'scale(1)';
        }
    });
    
    label.textContent = labels[rating];
    label.style.color = colors[rating];
    label.style.fontWeight = '900';
}

function resetStars() {
    const stars = document.querySelectorAll('.star-link');
    const label = document.getElementById('ratingLabel');
    
    stars.forEach(star => {
        star.style.color = '#d1d5db';
        star.style.transform = 'scale(1)';
    });
    
    label.textContent = 'Click to rate';
    label.style.color = '#9ca3af';
    label.style.fontWeight = '700';
}
