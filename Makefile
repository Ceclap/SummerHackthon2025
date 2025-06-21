.PHONY: help install install-dev run run-dev test test-cov clean lint format check-deps

# Переменные
PYTHON = python3
PIP = pip3
VENV = venv
APP_NAME = "AI Помощник Бухгалтера"

help: ## Показать справку
	@echo "$(APP_NAME) - Команды управления"
	@echo ""
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Установить зависимости
	@echo "📦 Установка зависимостей..."
	$(PIP) install -r requirements.txt
	@echo "✅ Зависимости установлены"

install-dev: ## Установить зависимости для разработки
	@echo "📦 Установка зависимостей для разработки..."
	$(PIP) install -r requirements.txt
	@echo "✅ Зависимости для разработки установлены"

check-deps: ## Проверить зависимости и Tesseract
	@echo "🔍 Проверка зависимостей..."
	@$(PYTHON) -c "import fastapi, uvicorn, pytesseract, fitz, PIL; print('✅ Все Python зависимости установлены')"
	@echo "🔍 Проверка Tesseract..."
	@$(PYTHON) -c "import pytesseract; print(f'✅ Tesseract версия: {pytesseract.get_tesseract_version()}')"

run: ## Запустить приложение в продакшн режиме
	@echo "🚀 Запуск $(APP_NAME) в продакшн режиме..."
	$(PYTHON) run.py

run-dev: ## Запустить приложение в режиме разработки
	@echo "🚀 Запуск $(APP_NAME) в режиме разработки..."
	$(PYTHON) run.py --reload --log-level debug

test: ## Запустить тесты
	@echo "🧪 Запуск тестов..."
	$(PYTHON) -m pytest test_main.py -v

test-cov: ## Запустить тесты с покрытием
	@echo "🧪 Запуск тестов с покрытием..."
	$(PYTHON) -m pytest test_main.py --cov=main --cov=config --cov-report=html --cov-report=term

lint: ## Проверить код с помощью flake8
	@echo "🔍 Проверка кода..."
	$(PYTHON) -m flake8 main.py config.py test_main.py run.py --max-line-length=100 --ignore=E501,W503

format: ## Форматировать код с помощью black
	@echo "🎨 Форматирование кода..."
	$(PYTHON) -m black main.py config.py test_main.py run.py --line-length=100

clean: ## Очистить временные файлы
	@echo "🧹 Очистка временных файлов..."
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf uploads/*
	rm -f app.log
	@echo "✅ Временные файлы удалены"

setup: ## Полная настройка проекта
	@echo "🔧 Полная настройка проекта..."
	@make install-dev
	@make check-deps
	@make clean
	@echo "✅ Проект настроен"

docker-build: ## Собрать Docker образ
	@echo "🐳 Сборка Docker образа..."
	docker build -t accounting-assistant .

docker-run: ## Запустить в Docker
	@echo "🐳 Запуск в Docker..."
	docker run -p 8000:8000 accounting-assistant

# Команды для разных ОС
install-tesseract-mac: ## Установить Tesseract на macOS
	@echo "📦 Установка Tesseract на macOS..."
	brew install tesseract
	brew install tesseract-lang
	@echo "✅ Tesseract установлен"

install-tesseract-ubuntu: ## Установить Tesseract на Ubuntu/Debian
	@echo "📦 Установка Tesseract на Ubuntu/Debian..."
	sudo apt update
	sudo apt install -y tesseract-ocr
	sudo apt install -y tesseract-ocr-ron tesseract-ocr-rus tesseract-ocr-eng
	@echo "✅ Tesseract установлен"

# Команды для мониторинга
logs: ## Показать логи приложения
	@echo "📋 Логи приложения:"
	@tail -f app.log

status: ## Проверить статус приложения
	@echo "🔍 Проверка статуса приложения..."
	@curl -s http://localhost:8000/health | $(PYTHON) -m json.tool

# Команды для разработки
dev-setup: ## Настройка окружения для разработки
	@echo "🔧 Настройка окружения для разработки..."
	@make install-dev
	@make check-deps
	@make format
	@make lint
	@echo "✅ Окружение для разработки настроено"

pre-commit: ## Выполнить проверки перед коммитом
	@echo "🔍 Выполнение проверок перед коммитом..."
	@make format
	@make lint
	@make test
	@echo "✅ Все проверки пройдены"

# Команды для продакшна
prod-setup: ## Настройка для продакшна
	@echo "🚀 Настройка для продакшна..."
	@make install
	@make check-deps
	@echo "✅ Продакшн окружение настроено"

prod-run: ## Запуск в продакшн режиме с несколькими воркерами
	@echo "🚀 Запуск в продакшн режиме..."
	$(PYTHON) run.py --workers 4 --log-level info 