const calendarBody = document.getElementById('calendar-body');
const calendarTitle = document.getElementById('calendar-title');
const prevMonthBtn = document.getElementById('prev-month');
const nextMonthBtn = document.getElementById('next-month');
const currentTimeElem = document.getElementById('current-time');
const futureTimeElem = document.getElementById('future-time');

const today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();

function generateCalendar(month, year) {
    const firstDay = (new Date(year, month, 1).getDay() + 6) % 7;
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    calendarBody.innerHTML = '';
    calendarTitle.textContent = `${new Date(year, month, 1).toLocaleString('ru', { month: 'long' })} ${year}`;

    let date = 1;
    let row = document.createElement('tr');
    for (let i = 0; i < firstDay; i++) {
        const cell = document.createElement('td');
        cell.innerHTML = '';
        row.appendChild(cell);
    }

    for (let i = 1; i <= daysInMonth; i++) {
        const cell = document.createElement('td');
        cell.textContent = i;
        if (i === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
            cell.classList.add('today');
        }
        row.appendChild(cell);

        if ((i + firstDay) % 7 === 0 || i === daysInMonth) {
            calendarBody.appendChild(row);
            row = document.createElement('tr');
        }
    }
}

function changeMonth(offset) {
    currentMonth += offset;
    if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    } else if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }
    generateCalendar(currentMonth, currentYear);
}

prevMonthBtn.addEventListener('click', () => changeMonth(-1));
nextMonthBtn.addEventListener('click', () => changeMonth(1));

generateCalendar(currentMonth, currentYear);

function updateTime() {
    const now = new Date();
    const futureTime = new Date(now.getTime() + 2 * 60 * 60 * 1000);

    currentTimeElem.textContent = `Текущее время: ${now.toLocaleTimeString('ru-RU', { hour12: false })}`;
    futureTimeElem.textContent = `Второе время: ${futureTime.toLocaleTimeString('ru-RU', { hour12: false })}`;
}

updateTime();
setInterval(updateTime, 1000);