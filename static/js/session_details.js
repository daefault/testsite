document.addEventListener('DOMContentLoaded', function () {
    const testSeat = document.querySelector('.seat-available');
    const seatMap = document.getElementById('seat-map');
    const cartSection = document.getElementById('cart-section');
    const selectedSeatsList = document.getElementById('selected-seats-list');
    const totalPriceSummary = document.getElementById('total-price-summary');
    const totalPriceDisplay = document.getElementById('total-price-display');
    const selectedCountElement = document.getElementById('selected-count');
    const availableSeatsElement = document.getElementById('available-seats');
    const confirmButton = document.getElementById('confirm-booking');
    const selectedSeatsInput = document.getElementById('selected-seats-input');
    const pricePerSeat = parseFloat(document.getElementById('price-per-seat').value);

    let selectedSeats = [];
    let totalPrice = 0;

    const initialAvailableSeats = parseInt(availableSeatsElement.textContent);
    let currentAvailableSeats = initialAvailableSeats;
    console.log("Проверка первого места:");
    const firstSeat = document.querySelector('.seat');
    if (firstSeat) {
        console.log("data-seat-id:", firstSeat.getAttribute('data-seat-id'));
        console.log("data-row:", firstSeat.getAttribute('data-row'));
        console.log("data-seat:", firstSeat.getAttribute('data-seat'));
    }
    seatMap.addEventListener('click', function (e) {
        const seat = e.target.closest('.seat');
        if (!seat) return;

        const seatKey = seat.getAttribute('data-seat-key');
        const row = seat.getAttribute('data-row');
        const seatNum = seat.getAttribute('data-seat');
        const price = parseFloat(seat.getAttribute('data-price')) || pricePerSeat;


        if (seat.classList.contains('seat-taken')) {
            alert('Это место уже занято!');
            return;
        }

        if (seat.classList.contains('seat-selected')) {
            seat.classList.remove('seat-selected');
            seat.classList.add('seat-available');
            selectedSeats = selectedSeats.filter(s => s.key !== seatKey); 
            currentAvailableSeats++;
        } else if (seat.classList.contains('seat-available')) {
            seat.classList.remove('seat-available');
            seat.classList.add('seat-selected');
            selectedSeats.push({
                key: seatKey,  
                row: row,
                seat: seatNum,
                price: price
            });
            currentAvailableSeats--;
        }

        console.log('Выбранные места:', selectedSeats);
        updateCart();
    });

    function updateCart() {
        cartSection.style.display = selectedSeats.length > 0 ? 'block' : 'none';

        selectedSeatsList.innerHTML = '';
        totalPrice = 0;

        selectedSeats.forEach(seat => {
            totalPrice += seat.price;

            const seatElement = document.createElement('div');
            seatElement.className = 'd-flex justify-content-between align-items-center mb-2 p-2 border rounded';
            seatElement.innerHTML = `
            <div>
                <i class="bi bi-ticket-perforated me-2"></i>
                <strong>Ряд ${seat.row}, Место ${seat.seat}</strong>
            </div>
            <div>
                <span class="text-success fw-bold">${seat.price} ₽</span>
            </div>
        `;
            selectedSeatsList.appendChild(seatElement);
        });

        if (totalPriceSummary) totalPriceSummary.textContent = totalPrice.toFixed(2);
        if (totalPriceDisplay) totalPriceDisplay.textContent = totalPrice.toFixed(2) + ' ₽';
        if (selectedCountElement) selectedCountElement.textContent = selectedSeats.length;

        if (availableSeatsElement) availableSeatsElement.textContent = Math.max(0, currentAvailableSeats);

        if (confirmButton) confirmButton.disabled = selectedSeats.length === 0;

        if (selectedSeatsInput) {
            const validSeats = selectedSeats.filter(s => s.key && typeof s.key === 'string' && s.key.includes('_'));
            const seatKeys = validSeats.map(s => s.key);

            if (seatKeys.length > 0) {
                selectedSeatsInput.value = JSON.stringify(seatKeys);
            } else {
                selectedSeatsInput.value = '[]';
            }
        }
    }

    const buyForm = document.getElementById('buy-tickets-form');
    if (buyForm) {
        buyForm.addEventListener('submit', function (e) {
            if (selectedSeats.length === 0) {
                e.preventDefault();
                alert('Выберите хотя бы одно место!');
                return;
            }

            const confirmBuy = confirm(
                `Подтвердить покупку ${selectedSeats.length} билетов?\n` +
                `Общая сумма: ${totalPrice} ₽`
            );

            if (!confirmBuy) {
                e.preventDefault();
            }
        });
    }
});