document.addEventListener('DOMContentLoaded', function () {
    // Инициализация переменных
    console.log('🎬 Загружен session_details.js');
    console.log('Проверка первого места:');
    const testSeat = document.querySelector('.seat-available');
    if (testSeat) {
        console.log('data-seat-key:', testSeat.getAttribute('data-seat-key'));
        console.log('data-row:', testSeat.getAttribute('data-row'));
        console.log('data-seat:', testSeat.getAttribute('data-seat'));
    }
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

    // Изначальное количество свободных мест
    const initialAvailableSeats = parseInt(availableSeatsElement.textContent);
    let currentAvailableSeats = initialAvailableSeats;

    // Проверяем, есть ли data-атрибуты
    console.log("Проверка первого места:");
    const firstSeat = document.querySelector('.seat');
    if (firstSeat) {
        console.log("data-seat-id:", firstSeat.getAttribute('data-seat-id'));
        console.log("data-row:", firstSeat.getAttribute('data-row'));
        console.log("data-seat:", firstSeat.getAttribute('data-seat'));
    }

    // Обработчик кликов
    seatMap.addEventListener('click', function (e) {
        const seat = e.target.closest('.seat');
        if (!seat) return;

        // Получаем данные из data-атрибутов - ИСПРАВЛЕНО
        const seatKey = seat.getAttribute('data-seat-key');  // Изменено с data-seat-id
        const row = seat.getAttribute('data-row');
        const seatNum = seat.getAttribute('data-seat');
        const price = parseFloat(seat.getAttribute('data-price')) || pricePerSeat;


        // Проверяем, не занято ли место
        if (seat.classList.contains('seat-taken')) {
            alert('Это место уже занято!');
            return;
        }

        // Переключаем выбор
        if (seat.classList.contains('seat-selected')) {
            // Отмена выбора
            seat.classList.remove('seat-selected');
            seat.classList.add('seat-available');
            selectedSeats = selectedSeats.filter(s => s.key !== seatKey);  // Исправлено s.id на s.key
            currentAvailableSeats++;
        } else if (seat.classList.contains('seat-available')) {
            // Выбор места
            seat.classList.remove('seat-available');
            seat.classList.add('seat-selected');
            selectedSeats.push({
                key: seatKey,  // Исправлено id на key
                row: row,
                seat: seatNum,
                price: price
            });
            currentAvailableSeats--;
        }

        console.log('Выбранные места:', selectedSeats); // Для отладки
        updateCart();
    });

    function updateCart() {
        // Показываем/скрываем корзину
        cartSection.style.display = selectedSeats.length > 0 ? 'block' : 'none';

        // Обновляем список мест
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

        // Обновляем итоговую сумму
        if (totalPriceSummary) totalPriceSummary.textContent = totalPrice.toFixed(2);
        if (totalPriceDisplay) totalPriceDisplay.textContent = totalPrice.toFixed(2) + ' ₽';
        if (selectedCountElement) selectedCountElement.textContent = selectedSeats.length;

        // Обновляем количество свободных мест
        if (availableSeatsElement) availableSeatsElement.textContent = Math.max(0, currentAvailableSeats);

        // Активируем/деактивируем кнопку
        if (confirmButton) confirmButton.disabled = selectedSeats.length === 0;

        // Заполняем скрытое поле для формы - ИСПРАВЛЕНО
        if (selectedSeatsInput) {
            // Фильтруем только места с корректным ключом
            const validSeats = selectedSeats.filter(s => s.key && typeof s.key === 'string' && s.key.includes('_'));
            const seatKeys = validSeats.map(s => s.key);

            if (seatKeys.length > 0) {
                // Отправляем строку JSON, НЕ двойной JSON!
                selectedSeatsInput.value = JSON.stringify(seatKeys);
                console.log('✅ Отправляемые данные:', selectedSeatsInput.value);
            } else {
                selectedSeatsInput.value = '[]'; // Пустой массив
                console.log('⚠️ Нет валидных мест для отправки');
            }
        }
    }

    // Обработчик отправки формы
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