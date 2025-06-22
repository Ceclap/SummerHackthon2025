// Toast Notification System
class ToastManager {
    constructor() {
        this.container = this.createContainer();
        this.toasts = [];
    }

    createContainer() {
        const container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
        return container;
    }

    show(options) {
        const {
            title = '',
            message = '',
            type = 'info',
            duration = 5000,
            closable = true
        } = options;

        const toast = this.createToast(title, message, type, closable);
        this.container.appendChild(toast);
        this.toasts.push(toast);

        // Trigger animation
        requestAnimationFrame(() => {
            toast.style.transform = 'translateX(0)';
            toast.style.opacity = '1';
        });

        // Auto remove
        if (duration > 0) {
            setTimeout(() => {
                this.remove(toast);
            }, duration);
        }

        return toast;
    }

    createToast(title, message, type, closable) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icon = this.getIcon(type);
        
        toast.innerHTML = `
            <div class="toast-icon">
                <i class="${icon}"></i>
            </div>
            <div class="toast-content">
                ${title ? `<div class="toast-title">${title}</div>` : ''}
                ${message ? `<div class="toast-message">${message}</div>` : ''}
            </div>
            ${closable ? '<button class="toast-close"><i class="fas fa-times"></i></button>' : ''}
        `;

        // Close button handler
        const closeBtn = toast.querySelector('.toast-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                this.remove(toast);
            });
        }

        return toast;
    }

    getIcon(type) {
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };
        return icons[type] || icons.info;
    }

    remove(toast) {
        if (!toast || !toast.parentNode) return;

        toast.classList.add('removing');
        
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
            const index = this.toasts.indexOf(toast);
            if (index > -1) {
                this.toasts.splice(index, 1);
            }
        }, 300);
    }

    clear() {
        this.toasts.forEach(toast => this.remove(toast));
    }
}

// Loading Overlay System
class LoadingManager {
    constructor() {
        this.overlay = this.createOverlay();
    }

    createOverlay() {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="loading-content">
                <div class="loading-spinner"></div>
                <div class="loading-text">Загрузка...</div>
            </div>
        `;
        document.body.appendChild(overlay);
        return overlay;
    }

    show(text = 'Загрузка...') {
        const textElement = this.overlay.querySelector('.loading-text');
        if (textElement) {
            textElement.textContent = text;
        }
        this.overlay.classList.add('active');
    }

    hide() {
        this.overlay.classList.remove('active');
    }
}

// Form Validation System
class FormValidator {
    constructor(form) {
        this.form = form;
        this.init();
    }

    init() {
        this.form.addEventListener('submit', (e) => {
            if (!this.validate()) {
                e.preventDefault();
            }
        });

        // Real-time validation
        const inputs = this.form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', () => {
                this.validateField(input);
            });
            input.addEventListener('input', () => {
                this.clearFieldError(input);
            });
        });
    }

    validate() {
        let isValid = true;
        const inputs = this.form.querySelectorAll('input[required], textarea[required], select[required]');
        
        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });

        return isValid;
    }

    validateField(field) {
        const value = field.value.trim();
        const type = field.type;
        const required = field.hasAttribute('required');
        
        // Clear previous errors
        this.clearFieldError(field);

        // Required validation
        if (required && !value) {
            this.showFieldError(field, 'Это поле обязательно для заполнения');
            return false;
        }

        // Type-specific validation
        if (value) {
            switch (type) {
                case 'email':
                    if (!this.isValidEmail(value)) {
                        this.showFieldError(field, 'Введите корректный email адрес');
                        return false;
                    }
                    break;
                case 'url':
                    if (!this.isValidUrl(value)) {
                        this.showFieldError(field, 'Введите корректный URL');
                        return false;
                    }
                    break;
                case 'number':
                    if (isNaN(value)) {
                        this.showFieldError(field, 'Введите корректное число');
                        return false;
                    }
                    break;
            }
        }

        // Custom validation attributes
        if (field.hasAttribute('data-min-length')) {
            const minLength = parseInt(field.getAttribute('data-min-length'));
            if (value.length < minLength) {
                this.showFieldError(field, `Минимальная длина: ${minLength} символов`);
                return false;
            }
        }

        if (field.hasAttribute('data-max-length')) {
            const maxLength = parseInt(field.getAttribute('data-max-length'));
            if (value.length > maxLength) {
                this.showFieldError(field, `Максимальная длина: ${maxLength} символов`);
                return false;
            }
        }

        // Show success state
        this.showFieldSuccess(field);
        return true;
    }

    showFieldError(field, message) {
        field.classList.add('error');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'form-error';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i>${message}`;
        field.parentNode.appendChild(errorDiv);
    }

    showFieldSuccess(field) {
        field.classList.add('success');
        const successDiv = document.createElement('div');
        successDiv.className = 'form-success';
        successDiv.innerHTML = `<i class="fas fa-check-circle"></i>Поле заполнено корректно`;
        field.parentNode.appendChild(successDiv);
    }

    clearFieldError(field) {
        field.classList.remove('error', 'success');
        const errorDiv = field.parentNode.querySelector('.form-error');
        const successDiv = field.parentNode.querySelector('.form-success');
        if (errorDiv) errorDiv.remove();
        if (successDiv) successDiv.remove();
    }

    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    isValidUrl(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }
}

// Modal System
class ModalManager {
    constructor() {
        this.activeModal = null;
    }

    show(options) {
        const {
            title = '',
            content = '',
            size = 'medium',
            closable = true,
            onClose = null
        } = options;

        const modal = this.createModal(title, content, size, closable);
        document.body.appendChild(modal);

        // Show modal
        requestAnimationFrame(() => {
            modal.classList.add('active');
        });

        this.activeModal = modal;

        // Close handlers
        if (closable) {
            const overlay = modal.querySelector('.modal-overlay');
            const closeBtn = modal.querySelector('.modal-close');
            
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) {
                    this.close();
                }
            });

            if (closeBtn) {
                closeBtn.addEventListener('click', () => {
                    this.close();
                });
            }

            // ESC key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    this.close();
                }
            });
        }

        if (onClose) {
            modal.onClose = onClose;
        }

        return modal;
    }

    createModal(title, content, size, closable) {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        
        const sizeClass = size === 'large' ? 'modal-large' : size === 'small' ? 'modal-small' : '';
        
        modal.innerHTML = `
            <div class="modal ${sizeClass}">
                <div class="modal-header">
                    <h3 class="modal-title">${title}</h3>
                    ${closable ? '<button class="modal-close"><i class="fas fa-times"></i></button>' : ''}
                </div>
                <div class="modal-body">
                    ${content}
                </div>
            </div>
        `;

        return modal;
    }

    close() {
        if (!this.activeModal) return;

        this.activeModal.classList.remove('active');
        
        setTimeout(() => {
            if (this.activeModal && this.activeModal.parentNode) {
                if (this.activeModal.onClose) {
                    this.activeModal.onClose();
                }
                this.activeModal.parentNode.removeChild(this.activeModal);
                this.activeModal = null;
            }
        }, 300);
    }
}

// Initialize global instances
window.toastManager = new ToastManager();
window.loadingManager = new LoadingManager();
window.modalManager = new ModalManager();

// Utility functions
window.showToast = (options) => window.toastManager.show(options);
window.showLoading = (text) => window.loadingManager.show(text);
window.hideLoading = () => window.loadingManager.hide();
window.showModal = (options) => window.modalManager.show(options);
window.closeModal = () => window.modalManager.close();

// Auto-initialize form validation
document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        new FormValidator(form);
    });
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ToastManager,
        LoadingManager,
        FormValidator,
        ModalManager
    };
} 