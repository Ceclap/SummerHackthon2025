document.addEventListener('DOMContentLoaded', function() {

    // --- AI Assistant Form ---
    const aiForm = document.getElementById('ai-form');
    const aiQuestion = document.getElementById('ai-question');
    const aiResponse = document.getElementById('ai-response');
    const aiResponseContainer = document.getElementById('ai-response-container');
    const submitBtn = document.querySelector('.ai-submit-btn');

    if (aiForm) {
        aiForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const question = aiQuestion.value.trim();
            if (!question) {
                showError('Пожалуйста, введите вопрос');
                return;
            }

            // Show loading state
            setLoadingState(true);
            
            try {
                const res = await fetch('/ask_ai', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question })
                });
                const data = await res.json();
                if (res.ok) {
                    responseDiv.textContent = data.answer || 'Нет ответа от ИИ.';
                } else {
                    responseDiv.textContent = data.answer || 'Ошибка сервера.';
                }
            } catch (err) {
                responseDiv.textContent = 'Ошибка соединения с сервером.';
            } finally {
                setLoadingState(false);
            }
        });
    }

    function setLoadingState(isLoading) {
        if (submitBtn) {
            const btnText = submitBtn.querySelector('.btn-text');
            const btnIcon = submitBtn.querySelector('.btn-icon');
            
            if (isLoading) {
                btnText.textContent = 'Обработка...';
                btnIcon.textContent = '⏳';
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.7';
            } else {
                btnText.textContent = 'Спросить';
                btnIcon.textContent = '🤖';
                submitBtn.disabled = false;
                submitBtn.style.opacity = '1';
            }
        }
    }

    function showResponse(answer) {
        if (aiResponse && aiResponseContainer) {
            aiResponse.textContent = answer;
            aiResponseContainer.style.display = 'block';
            
            // Smooth animation
            aiResponseContainer.style.opacity = '0';
            aiResponseContainer.style.transform = 'translateY(10px)';
            
            setTimeout(() => {
                aiResponseContainer.style.transition = 'all 0.3s ease';
                aiResponseContainer.style.opacity = '1';
                aiResponseContainer.style.transform = 'translateY(0)';
            }, 10);
        }
    }

    function showError(message) {
        if (aiResponse && aiResponseContainer) {
            aiResponse.innerHTML = `<span style="color: var(--accent-red);">❌ ${message}</span>`;
            aiResponseContainer.style.display = 'block';
            
            // Shake animation for error
            aiResponseContainer.style.animation = 'shake 0.5s ease-in-out';
            setTimeout(() => {
                aiResponseContainer.style.animation = '';
            }, 500);
        }
    }

    // --- Chart.js Initializers ---
    const revenueChartCtx = document.getElementById('revenue-chart');
    if (revenueChartCtx) {
        new Chart(revenueChartCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Revenue',
                    data: [12000, 19000, 15000, 25000, 22000, 30000],
                    borderColor: '#58A6FF',
                    tension: 0.1,
                    fill: false
                }]
            },
            options: { scales: { y: { beginAtZero: true } } }
        });
    }

    const salesChartCtx = document.getElementById('sales-chart');
    if (salesChartCtx) {
        new Chart(salesChartCtx, {
            type: 'bar',
            data: {
                labels: ['Product A', 'Product B', 'Product C'],
                datasets: [{
                    label: 'Sales Quantity',
                    data: [45, 60, 35],
                    backgroundColor: ['#3FB950', '#58A6FF', '#6e40c9']
                }]
            },
            options: { scales: { y: { beginAtZero: true } } }
        });
    }

    // --- Modal for Tipuri de documente ---
    if (typeof documentsData !== 'undefined') {
        const modal = document.getElementById('doc-modal');
        const modalTitle = document.getElementById('modal-title');
        const modalDocList = document.getElementById('modal-doc-list');
        const seeAllLinks = document.querySelectorAll('.see-all');
        const closeModal = document.querySelector('.close-modal');

        seeAllLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const docTypeKey = this.dataset.doctype;
                const docTypeData = documentsData[docTypeKey];
                if (docTypeData) {
                    modalTitle.textContent = docTypeData.name;
                    modalDocList.innerHTML = '';
                    docTypeData.docs.forEach(doc => {
                        const li = document.createElement('li');
                        li.innerHTML = `<span>${doc.id}</span><span>${doc.date}</span><a href="#" class="btn-vezi">Vezi</a>`;
                        modalDocList.appendChild(li);
                    });
                    modal.style.display = 'block';
                }
            });
        });

        if (closeModal) {
            closeModal.addEventListener('click', () => modal.style.display = 'none');
        }
        window.addEventListener('click', (event) => {
            if (event.target == modal) modal.style.display = 'none';
        });
    }

    // --- Drag and Drop for Upload ---
    const dropZone = document.querySelector('.drop-zone');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');

    if (dropZone) {
        dropZone.addEventListener('click', () => fileInput.click());
        browseBtn.addEventListener('click', () => fileInput.click());

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.style.borderColor = '#58A6FF';
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.style.borderColor = '#30363D';
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.style.borderColor = '#30363D';
            const files = e.dataTransfer.files;
            if (files.length) {
                fileInput.files = files;
                // Optionally, submit form automatically
                // document.getElementById('upload-form').submit();
            }
        });
    }
});

// Smooth scrolling for navigation
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    .stat-card:hover .stat-icon {
        animation: pulse 1s ease-in-out;
    }
    
    .feature-card:hover {
        animation: fadeIn 0.3s ease-out;
    }
`;
document.head.appendChild(style);

// Add smooth transitions to all interactive elements
document.addEventListener('DOMContentLoaded', function() {
    const interactiveElements = document.querySelectorAll('button, a, .card, .stat-card, .feature-card');
    
    interactiveElements.forEach(element => {
        element.style.transition = 'all 0.3s ease';
    });
});

// Auto-hide flash messages
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash');
    
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
});

// Language switcher enhancement
document.addEventListener('DOMContentLoaded', function() {
    const langButtons = document.querySelectorAll('.lang-btn');
    
    langButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            // Add loading state
            this.style.opacity = '0.7';
            this.style.pointerEvents = 'none';
            
            // Reset after navigation
            setTimeout(() => {
                this.style.opacity = '1';
                this.style.pointerEvents = 'auto';
            }, 1000);
        });
    });
});

function setTheme(theme) {
    document.body.classList.remove('theme-dark', 'theme-light', 'theme-blue');
    document.body.classList.add('theme-' + theme);
    localStorage.setItem('theme', theme);
}

function applySavedTheme() {
    const theme = localStorage.getItem('theme') || 'dark';
    setTheme(theme);
}

document.addEventListener('DOMContentLoaded', function() {
    applySavedTheme();
    const themeSelect = document.getElementById('themeSelect');
    if (themeSelect) {
        // Установить select в сохранённую тему
        const saved = localStorage.getItem('theme') || 'dark';
        themeSelect.value = saved;
        themeSelect.addEventListener('change', function() {
            setTheme(this.value);
        });
    }
});
