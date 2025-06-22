document.addEventListener('DOMContentLoaded', function() {
    // Инициализация графиков
    initCharts();
    
    // Инициализация AI помощника
    initAIAssistant();
    
    // Инициализация анимаций
    initAnimations();
    
    // Инициализация поиска и фильтрации
    initSearchAndFilter();
    
    // Инициализация уведомлений
    initNotifications();

    const modal = document.getElementById('doc-modal');
    if (!modal) return;

    const docCards = document.querySelectorAll('.recent-doc-item');
    const closeModalBtn = modal.querySelector('.close-modal');
    const modalTitle = modal.querySelector('#modal-title');
    const modalDetails = modal.querySelector('#modal-doc-details');

    docCards.forEach(card => {
        card.addEventListener('click', () => {
            const docType = card.dataset.docType;
            const docId = card.dataset.docId;
            const docDate = card.dataset.docDate;
            const filename = card.dataset.filename;

            modalTitle.textContent = docType;
            
            modalDetails.innerHTML = `
                <div class="modal-doc-line">
                    <span>${docId}</span>
                    <span>${docDate}</span>
                    <a href="/result/${filename}" class="btn-primary">${modal.dataset.viewText || 'Vezi'}</a>
                </div>
            `;
            
            modal.style.display = 'flex';
        });
    });

    const closeModal = () => {
        modal.style.display = 'none';
    };

    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeModal);
    }

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            closeModal();
        }
    });
});

function initCharts() {
    // График активности за неделю
    const activityCtx = document.getElementById('activityChart');
    if (activityCtx) {
        const activityChart = new Chart(activityCtx, {
            type: 'line',
            data: {
                labels: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
                datasets: [{
                    label: 'Документы',
                    data: [12, 19, 15, 25, 22, 18, 14],
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    // График типов документов
    const docTypesCtx = document.getElementById('docTypesChart');
    if (docTypesCtx) {
        const docTypesChart = new Chart(docTypesCtx, {
            type: 'doughnut',
            data: {
                labels: ['Фактуры', 'Боны', 'Другие'],
                datasets: [{
                    data: [45, 35, 20],
                    backgroundColor: [
                        'rgb(59, 130, 246)',
                        'rgb(34, 197, 94)',
                        'rgb(251, 146, 60)'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

function initAIAssistant() {
    const aiForm = document.getElementById('aiForm');
    const aiInput = document.getElementById('aiInput');
    const aiMessages = document.getElementById('aiMessages');

    if (aiForm && aiInput) {
        aiForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const message = aiInput.value.trim();
            if (!message) return;

            // Добавляем сообщение пользователя
            addAIMessage('user', message);
            aiInput.value = '';

            // Показываем индикатор загрузки
            const loadingMessage = addAIMessage('assistant', 'Печатаю...', true);

            try {
                const response = await fetch('/ask_ai', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                
                if (data.success) {
                    // Обновляем сообщение с ответом
                    updateAIMessage(loadingMessage, data.response);
                    showToast({
                        title: 'AI Помощник',
                        message: 'Ответ получен',
                        type: 'success'
                    });
                } else {
                    updateAIMessage(loadingMessage, 'Извините, произошла ошибка. Попробуйте еще раз.');
                    showToast({
                        title: 'Ошибка',
                        message: data.error || 'Не удалось получить ответ',
                        type: 'error'
                    });
                }
            } catch (error) {
                updateAIMessage(loadingMessage, 'Ошибка соединения. Проверьте интернет-соединение.');
                showToast({
                    title: 'Ошибка',
                    message: 'Проблема с соединением',
                    type: 'error'
                });
            }
        });
    }
}

function addAIMessage(type, content, isLoading = false) {
    const aiMessages = document.getElementById('aiMessages');
    if (!aiMessages) return null;

    const messageDiv = document.createElement('div');
    messageDiv.className = `ai-message ${type}`;
    
    const avatar = type === 'user' ? '👤' : '🤖';
    const time = new Date().toLocaleTimeString();
    
    messageDiv.innerHTML = `
        <div class="ai-message-avatar">${avatar}</div>
        <div class="ai-message-content">
            <div>${content}</div>
            <div class="ai-message-time">${time}</div>
        </div>
    `;

    if (isLoading) {
        messageDiv.classList.add('loading');
    }

    aiMessages.appendChild(messageDiv);
    aiMessages.scrollTop = aiMessages.scrollHeight;
    
    return messageDiv;
}

function updateAIMessage(messageDiv, content) {
    if (!messageDiv) return;
    
    messageDiv.classList.remove('loading');
    const contentDiv = messageDiv.querySelector('.ai-message-content div:first-child');
    if (contentDiv) {
        contentDiv.textContent = content;
    }
}

function initSearchAndFilter() {
    const searchInput = document.getElementById('docSearch');
    const filterSelect = document.getElementById('docFilter');
    const docsGrid = document.getElementById('docsGrid');

    if (!searchInput || !filterSelect || !docsGrid) return;

    function filterDocuments() {
        const searchTerm = searchInput.value.toLowerCase();
        const filterType = filterSelect.value;
        const docItems = docsGrid.querySelectorAll('.doc-item');

        docItems.forEach(item => {
            const docName = item.getAttribute('data-name') || '';
            const docType = item.getAttribute('data-type') || '';
            
            const matchesSearch = docName.includes(searchTerm);
            const matchesFilter = !filterType || docType === filterType;
            
            if (matchesSearch && matchesFilter) {
                item.classList.remove('hidden');
            } else {
                item.classList.add('hidden');
            }
        });

        // Показываем пустое состояние если нет результатов
        const visibleItems = docsGrid.querySelectorAll('.doc-item:not(.hidden)');
        const emptyState = docsGrid.querySelector('.empty-state');
        
        if (visibleItems.length === 0 && emptyState) {
            emptyState.style.display = 'block';
        } else if (emptyState) {
            emptyState.style.display = 'none';
        }
    }

    searchInput.addEventListener('input', filterDocuments);
    filterSelect.addEventListener('change', filterDocuments);
}

function initNotifications() {
    // Показываем приветственное уведомление
    setTimeout(() => {
        showToast({
            title: 'Добро пожаловать!',
            message: 'ContaSfera готова помочь с вашими документами',
            type: 'info',
            duration: 4000
        });
    }, 1000);
}

function initAnimations() {
    // Анимация появления статистических карточек
    const statCards = document.querySelectorAll('.stat-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    statCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });

    // Анимация появления документов
    const docItems = document.querySelectorAll('.doc-item');
    docItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateX(-20px)';
        item.style.transition = 'all 0.4s ease';
        
        setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
        }, index * 100);
    });
}

// Функции для работы с документами
function viewDocument(filename) {
    showLoading('Загрузка документа...');
    
    // Имитация загрузки
    setTimeout(() => {
        hideLoading();
        showModal({
            title: `Просмотр документа: ${filename}`,
            content: `
                <div style="text-align: center; padding: 40px;">
                    <i class="fas fa-file-alt" style="font-size: 4rem; color: var(--accent-primary); margin-bottom: 20px;"></i>
                    <h3>${filename}</h3>
                    <p>Функция просмотра документов находится в разработке</p>
                    <div style="margin-top: 20px;">
                        <button class="btn btn-primary" onclick="downloadDocument('${filename}')">
                            <i class="fas fa-download"></i> Скачать
                        </button>
                    </div>
                </div>
            `,
            size: 'medium'
        });
    }, 1000);
}

function downloadDocument(filename) {
    showLoading('Подготовка файла...');
    
    fetch(`/download/${filename}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        }
        throw new Error('Ошибка загрузки');
    })
    .then(blob => {
        hideLoading();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showToast({
            title: 'Успешно',
            message: `Файл ${filename} скачан`,
            type: 'success'
        });
    })
    .catch(error => {
        hideLoading();
        showToast({
            title: 'Ошибка',
            message: 'Не удалось скачать файл',
            type: 'error'
        });
    });
}

// Глобальные функции для использования в HTML
window.viewDocument = viewDocument;
window.downloadDocument = downloadDocument;

// Функция для обновления статистики в реальном времени
function updateStats() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const finalValue = stat.textContent;
        const isPercentage = finalValue.includes('%');
        const isCurrency = finalValue.includes('₼');
        
        let numericValue = parseFloat(finalValue.replace(/[^\d.]/g, ''));
        let currentValue = 0;
        const increment = numericValue / 50;
        
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= numericValue) {
                currentValue = numericValue;
                clearInterval(timer);
            }
            
            if (isPercentage) {
                stat.textContent = currentValue.toFixed(1) + '%';
            } else if (isCurrency) {
                stat.textContent = '₼ ' + Math.floor(currentValue).toLocaleString();
            } else {
                stat.textContent = Math.floor(currentValue).toLocaleString();
            }
        }, 30);
    });
}

// Запускаем анимацию статистики при загрузке страницы
setTimeout(updateStats, 500);

// Добавляем интерактивность к карточкам документов
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn-vezi')) {
        const docName = e.target.getAttribute('data-doc');
        showDocumentModal(docName);
    }
});

function showDocumentModal(docName) {
    // Создаем модальное окно для просмотра документа
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>Просмотр документа: ${docName}</h3>
                <button class="close-modal">&times;</button>
            </div>
            <div class="modal-body">
                <p>Здесь будет отображаться содержимое документа ${docName}</p>
                <div class="modal-actions">
                    <button class="btn btn-primary">Редактировать</button>
                    <button class="btn btn-secondary">Скачать</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Обработчик закрытия
    modal.addEventListener('click', function(e) {
        if (e.target === modal || e.target.classList.contains('close-modal')) {
            document.body.removeChild(modal);
        }
    });
} 