document.addEventListener('DOMContentLoaded', function() {
    initMovieCards();
    initSessionFilters();
    initBookingSystem();
    initRatingSystem();
});


function initMovieCards() {
    const movieCards = document.querySelectorAll('.movie-card');
    
    movieCards.forEach(card => {

        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = '0 15px 30px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.08)';
        });
        
        const poster = card.querySelector('.movie-poster');
        if (poster) {
            poster.addEventListener('click', function(e) {
                e.preventDefault();
                const movieId = this.closest('.movie-card').dataset.movieId;
                if (movieId) {
                    window.location.href = `/movies/${movieId}/`;
                }
            });
        }
    });
}

function initSessionFilters() {
    const dateFilter = document.getElementById('date-filter');
    const movieFilter = document.getElementById('movie-filter');
    
    if (dateFilter) {
        dateFilter.addEventListener('change', function() {
            this.form.submit();
        });
    }
    
    if (movieFilter) {
        movieFilter.addEventListener('change', function() {
            this.form.submit();
        });
    }
    
    const dateInputs = document.querySelectorAll('.datepicker');
    dateInputs.forEach(input => {
        if (input.type === 'text') {
            input.type = 'date';
        }
    });
}

function initBookingSystem() {
    const bookButtons = document.querySelectorAll('.btn-book');
    
    bookButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const sessionId = this.dataset.sessionId;
            const movieTitle = this.dataset.movieTitle;
            
            if (sessionId) {
                showSeatSelection(sessionId, movieTitle);
            }
        });
    });
}

function initRatingSystem() {
    const ratingStars = document.querySelectorAll('.rating-star');
    
    ratingStars.forEach(star => {
        star.addEventListener('click', function() {
            const rating = this.dataset.rating;
            const movieId = this.dataset.movieId;
            
            if (rating && movieId) {
                submitRating(movieId, rating);
            }
        });
        
        star.addEventListener('mouseenter', function() {
            const rating = parseInt(this.dataset.rating);
            highlightStars(rating);
        });
        
        star.addEventListener('mouseleave', function() {
            resetStars();
        });
    });
}

function showSeatSelection(sessionId, movieTitle) {
    console.log(`Выбор мест для сеанса ${sessionId}: ${movieTitle}`);
}

function submitRating(movieId, rating) {
    fetch(`/api/movies/${movieId}/rate/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ rating: rating })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            CinemaUtils.showToast('Спасибо за оценку!', 'success');
            updateRatingDisplay(movieId, data.new_rating);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        CinemaUtils.showToast('Ошибка при оценке', 'danger');
    });
}

function highlightStars(rating) {
    const stars = document.querySelectorAll('.rating-star');
    stars.forEach(star => {
        if (parseInt(star.dataset.rating) <= rating) {
            star.classList.add('text-warning');
        } else {
            star.classList.remove('text-warning');
        }
    });
}

function resetStars() {
    const stars = document.querySelectorAll('.rating-star');
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateRatingDisplay(movieId, newRating) {
    const ratingElement = document.querySelector(`.movie-rating[data-movie-id="${movieId}"]`);
    if (ratingElement) {
        ratingElement.textContent = newRating;
    }
}

window.Cinema = {
    initBookingSystem,
    submitRating,
    showSeatSelection
};