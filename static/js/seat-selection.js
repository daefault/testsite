// static/js/seat-selection.js

class SeatSelection {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.selectedSeats = new Set();
        this.totalPrice = 0;
        
        if (this.container) {
            this.init();
        }
    }
    
    init() {
        this.bindEvents();
        this.updateSummary();
    }
    
    bindEvents() {
        // Обработка кликов по местам
        this.container.addEventListener('click', (e) => {
            const seat = e.target.closest('.seat');
            if (seat && seat.classList.contains('seat-available')) {
                this.toggleSeat(seat);
            }
        });
        
        // Кнопка подтверждения
        const confirmBtn = document.getElementById('confirm-booking');
        if (confirmBtn) {
            confirmBtn.addEventListener('click', () => this.confirmBooking());
        }
        
        // Кнопка отмены
        const cancelBtn = document.getElementById('cancel-booking');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', () => this.cancelBooking());
        }
    }
    
    toggleSeat(seat) {
        const seatId = seat.dataset.seatId;
        
        if (this.selectedSeats.has(seatId)) {
            // Убираем из выбранных
            this.selectedSeats.delete(seatId);
            seat.classList.remove('seat-selected');
            seat.classList.add('seat-available');
        } else {
            // Добавляем в выбранные
            this.selectedSeats.add(seatId);
            seat.classList.remove('seat-available');
            seat.classList.add('seat-selected');
        }
        
        this.updateSummary();
    }
    
    updateSummary() {
        const seatCount = this.selectedSeats.size;
        const pricePerSeat = parseFloat(document.getElementById('price-per-seat').value) || 0;
        this.totalPrice = seatCount * pricePerSeat;
        
        // Обновляем отображение
        const countElement = document.getElementById('selected-seats-count');
        const priceElement = document.getElementById('total-price');
        const seatsListElement = document.getElementById('selected-seats-list');
        
        if (countElement) countElement.textContent = seatCount;
        if (priceElement) priceElement.textContent = this.totalPrice.toFixed(2);
        
        if (seatsListElement) {
            seatsListElement.innerHTML = '';
            this.selectedSeats.forEach(seatId => {
                const seatElement = document.querySelector(`[data-seat-id="${seatId}"]`);
                if (seatElement) {
                    const seatInfo = seatElement.dataset.seatInfo || seatId;
                    const li = document.createElement('li');
                    li.className = 'list-group-item d-flex justify-content-between align-items-center';
                    li.innerHTML = `
                        ${seatInfo}
                        <button class="btn btn-sm btn-outline-danger remove-seat" data-seat-id="${seatId}">
                            &times;
                        </button>
                    `;
                    seatsListElement.appendChild(li);
                }
            });
            
            // Добавляем обработчики для кнопок удаления
            seatsListElement.querySelectorAll('.remove-seat').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const seatId = e.target.closest('button').dataset.seatId;
                    this.removeSeat(seatId);
                });
            });
        }
        
        // Активируем/деактивируем кнопку подтверждения
        const confirmBtn = document.getElementById('confirm-booking');
        if (confirmBtn) {
            confirmBtn.disabled = seatCount === 0;
        }
    }
    
    removeSeat(seatId) {
        const seatElement = document.querySelector(`[data-seat-id="${seatId}"]`);
        if (seatElement) {
            seatElement.classList.remove('seat-selected');
            seatElement.classList.add('seat-available');
        }
        
        this.selectedSeats.delete(seatId);
        this.updateSummary();
    }
    
    confirmBooking() {
        if (this.selectedSeats.size === 0) {
            CinemaUtils.showToast('Выберите хотя бы одно место', 'warning');
            return;
        }
        
        const sessionId = document.getElementById('session-id').value;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch('/api/book-tickets/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                session_id: sessionId,
                seats: Array.from(this.selectedSeats)
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                CinemaUtils.showToast('Билеты успешно забронированы!', 'success');
                setTimeout(() => {
                    window.location.href = data.redirect_url;
                }, 2000);
            } else {
                CinemaUtils.showToast(data.error || 'Ошибка бронирования', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            CinemaUtils.showToast('Ошибка сети', 'danger');
        });
    }
    
    cancelBooking() {
        this.selectedSeats.clear();
        document.querySelectorAll('.seat-selected').forEach(seat => {
            seat.classList.remove('seat-selected');
            seat.classList.add('seat-available');
        });
        this.updateSummary();
        CinemaUtils.showToast('Выбор мест отменён', 'info');
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('seat-map')) {
        window.seatSelection = new SeatSelection('seat-map');
    }
});