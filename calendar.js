document.addEventListener('DOMContentLoaded', () => {
    const monthYearEl = document.getElementById('month-year');
    const weekdaysEl = document.getElementById('calendar-weekdays');
    const daysEl = document.getElementById('calendar-days');
    const prevMonthBtn = document.getElementById('prev-month-btn');
    const nextMonthBtn = document.getElementById('next-month-btn');
    const tasksDateEl = document.getElementById('tasks-date');
    const taskListEl = document.getElementById('task-list');

    if (!monthYearEl) return;

    let currentDate = new Date();
    let selectedDate = new Date();

    const mockTasks = {
        // "YYYY-MM-DD": ["Task 1", "Task 2"]
    };

    const today = new Date();
    const day = today.getDate();
    const month = today.getMonth() + 1;
    const year = today.getFullYear();
    
    // Add some dynamic mock tasks around today's date
    mockTasks[`${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`] = ["Проверить последнюю банковскую выписку", "Подготовить кассовый отчет"];
    mockTasks[`${year}-${String(month).padStart(2, '0')}-${String(day + 2).padStart(2, '0')}`] = ["Отправить счет-фактуру #1024 в 'Digital Solutions SRL'"];
    mockTasks[`${year}-${String(month).padStart(2, '0')}-${String(day + 5).padStart(2, '0')}`] = ["Крайний срок уплаты НДС"];
    if (day > 3) {
      mockTasks[`${year}-${String(month).padStart(2, '0')}-${String(day - 3).padStart(2, '0')}`] = ["Получение счета от 'Furnizor Electric'"];
    }


    const renderCalendar = () => {
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();

        const firstDayOfMonth = new Date(year, month, 1);
        const lastDateOfMonth = new Date(year, month + 1, 0);
        const lastDateOfLastMonth = new Date(year, month, 0);

        const monthNames = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"];
        monthYearEl.textContent = `${monthNames[month]} ${year}`;
        
        const weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"];
        weekdaysEl.innerHTML = weekdays.map(day => `<div>${day}</div>`).join('');
        
        daysEl.innerHTML = '';
        
        // Days from previous month
        let dayOfWeek = firstDayOfMonth.getDay();
        if (dayOfWeek === 0) { // Sunday
            dayOfWeek = 7;
        }

        for (let i = dayOfWeek; i > 1; i--) {
            const day = lastDateOfLastMonth.getDate() - i + 2;
            daysEl.innerHTML += `<div class="calendar-day prev-month">${day}</div>`;
        }

        // Days of current month
        for (let i = 1; i <= lastDateOfMonth.getDate(); i++) {
            const dayEl = document.createElement('div');
            dayEl.classList.add('calendar-day');
            dayEl.textContent = i;
            dayEl.dataset.date = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;

            const today = new Date();
            if (i === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
                dayEl.classList.add('today');
            }
            if (i === selectedDate.getDate() && month === selectedDate.getMonth() && year === selectedDate.getFullYear()) {
                dayEl.classList.add('selected');
            }
            if (mockTasks[dayEl.dataset.date]) {
                dayEl.classList.add('has-task');
            }
            daysEl.appendChild(dayEl);
        }

        // Click event for each day
        document.querySelectorAll('.calendar-day:not(.prev-month, .next-month)').forEach(day => {
            day.addEventListener('click', (e) => {
                document.querySelector('.calendar-day.selected')?.classList.remove('selected');
                e.currentTarget.classList.add('selected');
                selectedDate = new Date(e.currentTarget.dataset.date);
                renderTasks();
            });
        });
    };

    const renderTasks = () => {
        const dateKey = `${selectedDate.getFullYear()}-${String(selectedDate.getMonth() + 1).padStart(2, '0')}-${String(selectedDate.getDate()).padStart(2, '0')}`;
        tasksDateEl.textContent = `Задачи на ${selectedDate.toLocaleDateString('ru-RU', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}`;
        
        const tasks = mockTasks[dateKey];
        if (tasks && tasks.length > 0) {
            taskListEl.innerHTML = tasks.map(task => `<li>${task}</li>`).join('');
        } else {
            taskListEl.innerHTML = `<li class="no-tasks">Нет задач на этот день.</li>`;
        }
    };
    
    prevMonthBtn.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });

    nextMonthBtn.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });

    renderCalendar();
    renderTasks();
});
 