"""
Конфигурационный файл для AI Помощника Бухгалтера
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import Set

# Загружаем переменные окружения из .env файла
load_dotenv()

class Config:
    """Конфигурация приложения AI Помощник Бухгалтера."""
    
    # --- Основные настройки приложения ---
    APP_NAME = "AI Помощник Бухгалтера"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Интеллектуальный помощник для бухгалтеров в Молдове"
    
    # --- Настройки сервера ---
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # --- Настройки файлов ---
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    UPLOADS_DIR = "uploads"
    LOGS_DIR = "logs"
    LOG_FILE = "logs/app.log"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # --- Разрешенные форматы файлов ---
    ALLOWED_EXTENSIONS = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
    IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
    
    # --- OpenAI API настройки ---
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o"
    OPENAI_MAX_TOKENS = 4096
    OPENAI_TEMPERATURE = 0.1
    
    # --- Tesseract настройки (fallback) ---
    TESSERACT_LANGUAGES = "ron+rus+eng"
    TESSERACT_CONFIG = "--oem 3 --psm 6"
    
    # --- Порог уверенности для классификации ---
    CONFIDENCE_THRESHOLD = 0.1
    
    # --- CORS настройки ---
    CORS_ORIGINS = ["*"]
    CORS_METHODS = ["*"]
    CORS_HEADERS = ["*"]
    
    # --- Типы документов и ключевые слова ---
    DOCUMENT_TYPES = {
        "Factură/Счет": {
            "keywords": [
                "factură", "invoice", "счет", "счет-фактура", "фактура",
                "total", "итого", "suma", "сумма", "client", "клиент",
                "furnizor", "поставщик", "data", "дата", "nr", "номер"
            ]
        },
        "Chitanță/Квитанция": {
            "keywords": [
                "chitanță", "receipt", "квитанция", "платеж", "payment",
                "suma plătită", "оплачено", "data plății", "дата оплаты",
                "confirmare", "подтверждение", "achitat", "оплачен"
            ]
        },
        "Extras bancar/Банковская выписка": {
            "keywords": [
                "extras bancar", "bank statement", "банковская выписка",
                "cont bancar", "банковский счет", "sold", "баланс",
                "tranzacții", "транзакции", "operațiuni", "операции",
                "bancă", "банк", "codul contului", "код счета"
            ]
        },
        "Contract/Договор": {
            "keywords": [
                "contract", "договор", "acord", "соглашение", "parte",
                "сторона", "obligații", "обязательства", "termeni",
                "условия", "clauze", "пункты", "semnat", "подписан"
            ]
        },
        "Ordon de plată/Платежное поручение": {
            "keywords": [
                "ordon de plată", "платежное поручение", "transfer",
                "перевод", "beneficiar", "получатель", "suma transfer",
                "сумма перевода", "cont beneficiar", "счет получателя",
                "codul bancar", "банковский код"
            ]
        },
        "Notă de credit/Кредитное уведомление": {
            "keywords": [
                "notă de credit", "кредитное уведомление", "credit",
                "кредит", "acordare", "предоставление", "suma credit",
                "сумма кредита", "dobândă", "процент", "rata", "ставка"
            ]
        },
        "Notă de debit/Дебетовое уведомление": {
            "keywords": [
                "notă de debit", "дебетовое уведомление", "debit",
                "дебет", "scădere", "списание", "suma debit",
                "сумма дебета", "comision", "комиссия", "taxă", "налог"
            ]
        },
        "Certificat fiscal/Налоговый сертификат": {
            "keywords": [
                "certificat fiscal", "налоговый сертификат", "fiscal",
                "налоговый", "cod fiscal", "налоговый код", "an fiscal",
                "налоговый год", "impozit", "налог", "contribuții",
                "взносы", "autoritate fiscală", "налоговая служба"
            ]
        },
        "Declarație fiscală/Налоговая декларация": {
            "keywords": [
                "declarație fiscală", "налоговая декларация", "declarație",
                "декларация", "venituri", "доходы", "cheltuieli",
                "расходы", "impozit calculat", "исчисленный налог",
                "an fiscal", "налоговый год", "cod fiscal", "налоговый код"
            ]
        },
        "Raport financiar/Финансовый отчет": {
            "keywords": [
                "raport financiar", "финансовый отчет", "bilant",
                "баланс", "cont de profit și pierdere", "отчет о прибылях",
                "active", "активы", "pasive", "пассивы", "capital",
                "капитал", "rezultat", "результат", "perioada", "период"
            ]
        }
    }
    
    @classmethod
    def get_tesseract_path(cls) -> str:
        """Возвращает путь к Tesseract в зависимости от ОС."""
        import platform
        
        system = platform.system().lower()
        
        if system == "windows":
            return r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        elif system == "darwin":  # macOS
            # Проверяем разные возможные пути для macOS
            possible_paths = [
                "/opt/homebrew/bin/tesseract",  # Apple Silicon (M1/M2)
                "/usr/local/bin/tesseract",     # Intel Mac
                "/usr/bin/tesseract"            # System path
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    return path
                    
            # Если не найден, возвращаем стандартный путь
            return "/opt/homebrew/bin/tesseract"
        else:  # Linux
            return "/usr/bin/tesseract"
    
    @classmethod
    def create_directories(cls):
        """Создает необходимые директории."""
        Path(cls.UPLOADS_DIR).mkdir(exist_ok=True)
        Path(cls.LOGS_DIR).mkdir(exist_ok=True)
    
    @classmethod
    def validate_config(cls):
        """Проверяет валидность конфигурации."""
        import subprocess
        
        # Проверка Tesseract
        try:
            result = subprocess.run([cls.get_tesseract_path(), "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                print(f"✓ Tesseract найден: {version.split()[-1]}")
            else:
                print("⚠ Tesseract не найден или недоступен")
        except Exception as e:
            print(f"⚠ Ошибка проверки Tesseract: {e}")
        
        # Проверка OpenAI API ключа
        if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY == "your_openai_api_key_here":
            print("⚠ OpenAI API ключ не настроен. Используется Tesseract OCR.")
        else:
            print("✓ OpenAI API ключ настроен")
        
        # Проверка директорий
        cls.create_directories()
        print("✓ Конфигурация валидна")

# Создаем экземпляр конфигурации
config = Config() 