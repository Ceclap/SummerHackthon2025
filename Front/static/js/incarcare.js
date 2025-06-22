document.addEventListener('DOMContentLoaded', function() {
    // Элементы интерфейса
    const uploadArea = document.getElementById('upload-area');
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const selectFileBtn = document.getElementById('select-file-btn');
    const uploadProgress = document.getElementById('upload-progress');
    const progressBar = document.getElementById('progress-bar');
    const progressPercentage = document.getElementById('progress-percentage');
    const resultsSection = document.getElementById('results-section');
    const tableContainer = document.getElementById('table-container');
    const errorsContainer = document.getElementById('errors-container');
    const downloadExcelBtn = document.getElementById('download-excel-btn');
    const recheckBtn = document.getElementById('recheck-btn');
    const newDocumentBtn = document.getElementById('new-document-btn');
    const editModeBtn = document.getElementById('edit-mode-btn');
    const saveChangesBtn = document.getElementById('save-changes-btn');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const fileType = document.getElementById('file-type');

    // Состояние
    let currentTable = [];
    let currentFile = null;
    let isEditMode = false;

    // Инициализация
    initEventListeners();
    updateStep(1);

    function initEventListeners() {
        // Выбор файла
        selectFileBtn.addEventListener('click', () => fileInput.click());
        dropZone.addEventListener('click', () => fileInput.click());
        
        // Drag & Drop
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });

        dropZone.addEventListener('drop', handleDrop, false);
        fileInput.addEventListener('change', handleFileSelect);
        
        // Кнопки действий
        if (downloadExcelBtn) downloadExcelBtn.addEventListener('click', downloadExcel);
        if (recheckBtn) recheckBtn.addEventListener('click', recheckTable);
        if (newDocumentBtn) newDocumentBtn.addEventListener('click', resetToUpload);
        if (editModeBtn) editModeBtn.addEventListener('click', toggleEditMode);
        if (saveChangesBtn) saveChangesBtn.addEventListener('click', saveChanges);
    }

    // Drag & Drop
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight(e) {
        dropZone.classList.add('dragover');
    }

    function unhighlight(e) {
        dropZone.classList.remove('dragover');
    }

    function handleDrop(e) {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect();
        }
    }

    // Обработка выбора файла
    function handleFileSelect() {
        const file = fileInput.files[0];
        if (!file) return;

        // Проверка типа файла
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'application/pdf'];
        if (!allowedTypes.includes(file.type) && !file.name.match(/\.(pdf|png|jpg|jpeg|gif|webp)$/i)) {
            showNotification('Неподдерживаемый тип файла. Поддерживаются: PDF, PNG, JPG, JPEG, GIF, WEBP', 'error');
            return;
        }

        // Проверка размера файла (16MB)
        const maxSize = 16 * 1024 * 1024; // 16MB
        if (file.size > maxSize) {
            showNotification('Файл слишком большой. Максимальный размер: 16MB', 'error');
            return;
        }

        currentFile = file;
        processFile(file);
    }

    // Обработка файла
    function processFile(file) {
        updateStep(2);
        showLoading();
        
        const formData = new FormData();
        formData.append('file', file);

        fetch('/extract', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 302) {
                    // Перенаправление на страницу результатов
                    window.location.href = response.url;
                    return;
                }
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response.text();
        })
        .then(data => {
            hideLoading();
            
            // Если получили HTML (перенаправление), просто следуем по ссылке
            if (data.includes('<!DOCTYPE html>') || data.includes('<html>')) {
                // Это HTML страница, значит перенаправление уже произошло
                return;
            }
            
            // Пытаемся распарсить JSON
            try {
                const jsonData = JSON.parse(data);
                if (jsonData.error) {
                    showNotification('Ошибка: ' + jsonData.error, 'error');
                    return;
                }
            } catch (e) {
                // Если не JSON, значит это перенаправление
                console.log('Получен ответ, который не является JSON');
            }
        })
        .catch(error => {
            hideLoading();
            console.error('Ошибка:', error);
            showNotification('Произошла ошибка при обработке файла. Попробуйте еще раз.', 'error');
        });
    }

    // Показать загрузку
    function showLoading() {
        uploadProgress.style.display = 'block';
        dropZone.style.display = 'none';
        
        // Анимация прогресса
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            progressBar.style.width = progress + '%';
            progressPercentage.textContent = Math.round(progress) + '%';
        }, 200);
        
        // Сохраняем interval для остановки
        window.progressInterval = interval;
    }

    // Скрыть загрузку
    function hideLoading() {
        if (window.progressInterval) {
            clearInterval(window.progressInterval);
        }
        uploadProgress.style.display = 'none';
        dropZone.style.display = 'block';
        progressBar.style.width = '0%';
        progressPercentage.textContent = '0%';
    }

    // Показать результаты
    function showResults(file, table, errors) {
        // Информация о файле
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        fileType.textContent = file.type || 'Неизвестный тип';
        
        // Рендерим таблицу
        renderTable(table);
        
        // Показываем ошибки
        renderErrors(errors);
        
        // Показываем секцию результатов
        resultsSection.style.display = 'block';
        updateStep(4);
    }

    // Рендеринг таблицы
    function renderTable(table) {
        if (!table || !table.length) {
            tableContainer.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">Нет данных для отображения</p>';
            return;
        }

        let html = '<table class="data-table"><thead><tr>';
        
        // Заголовки
        const headers = Object.keys(table[0]);
        headers.forEach(header => {
            html += `<th>${escapeHtml(header)}</th>`;
        });
        html += '</tr></thead><tbody>';
        
        // Данные
        table.forEach(row => {
            html += '<tr>';
            headers.forEach(header => {
                html += `<td>${escapeHtml(row[header] || '')}</td>`;
            });
            html += '</tr>';
        });
        
        html += '</tbody></table>';
        tableContainer.innerHTML = html;
    }

    // Рендеринг ошибок
    function renderErrors(errors) {
        if (!errors || errors.length === 0) {
            errorsContainer.innerHTML = '<div class="success-message"><i class="fas fa-check-circle"></i> Документ прошел проверку</div>';
            return;
        }

        let html = '';
        errors.forEach(error => {
            html += `<div class="error-item">
                <i class="fas fa-exclamation-triangle"></i>
                <span>${escapeHtml(error)}</span>
            </div>`;
        });
        errorsContainer.innerHTML = html;
    }

    // Переключение режима редактирования
    function toggleEditMode() {
        isEditMode = !isEditMode;
        
        if (isEditMode) {
            editModeBtn.style.display = 'none';
            saveChangesBtn.style.display = 'inline-block';
            tableContainer.querySelectorAll('td').forEach(cell => {
                cell.contentEditable = true;
                cell.classList.add('editable');
            });
        } else {
            editModeBtn.style.display = 'inline-block';
            saveChangesBtn.style.display = 'none';
            tableContainer.querySelectorAll('td').forEach(cell => {
                cell.contentEditable = false;
                cell.classList.remove('editable');
            });
        }
    }

    // Сохранение изменений
    function saveChanges() {
        currentTable = collectTableData();
        toggleEditMode();
        showNotification('Изменения сохранены', 'success');
    }

    // Сбор данных таблицы
    function collectTableData() {
        const table = tableContainer.querySelector('table');
        const rows = table.querySelectorAll('tbody tr');
        const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent);
        
        return Array.from(rows).map(row => {
            const cells = row.querySelectorAll('td');
            const rowData = {};
            headers.forEach((header, index) => {
                rowData[header] = cells[index] ? cells[index].textContent : '';
            });
            return rowData;
        });
    }

    // Повторная проверка
    function recheckTable() {
        showNotification('Проверка выполняется...', 'info');
        // Здесь можно добавить логику повторной проверки
    }

    // Скачивание Excel
    function downloadExcel() {
        const data = isEditMode ? collectTableData() : currentTable;
        
        fetch(`/download/${currentFile.name}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${currentFile.name.replace(/\.[^/.]+$/, '')}_edited.xlsx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            showNotification('Файл успешно скачан', 'success');
        })
        .catch(error => {
            console.error('Ошибка скачивания:', error);
            showNotification('Ошибка при скачивании файла', 'error');
        });
    }

    // Сброс к загрузке
    function resetToUpload() {
        resultsSection.style.display = 'none';
        uploadArea.style.display = 'block';
        dropZone.style.display = 'block';
        fileInput.value = '';
        currentFile = null;
        currentTable = [];
        isEditMode = false;
        updateStep(1);
    }

    // Обновление шага
    function updateStep(stepNumber) {
        document.querySelectorAll('.step').forEach((step, index) => {
            if (index + 1 <= stepNumber) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });
    }

    // Форматирование размера файла
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Экранирование HTML
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Показать уведомление
    function showNotification(message, type = 'info') {
        // Используем существующую систему уведомлений
        if (window.showToast) {
            window.showToast(message, type);
        } else {
            alert(message);
        }
    }
}); 