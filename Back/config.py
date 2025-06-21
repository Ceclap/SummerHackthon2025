"""
Конфигурационный файл для AI Помощника Бухгалтера
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import Set, Dict, List, Optional
from dataclasses import dataclass

# Загружаем переменные окружения из .env файла
load_dotenv()

@dataclass
class LanguageConfig:
    """Конфигурация для поддержки языков"""
    code: str
    name: str
    flag: str
    date_format: str
    currency: str
    currency_symbol: str

@dataclass
class DocumentTypeConfig:
    """Конфигурация типов документов для Молдовы"""
    type_id: str
    name_ro: str
    name_ru: str
    keywords_ro: List[str]
    keywords_ru: List[str]
    required_fields: List[str]
    fiscal_code: Optional[str] = None

class Config:
    """Конфигурация приложения для бухгалтеров Молдовы"""
    
    # Основные настройки
    APP_NAME = "AI Помощник Бухгалтера Молдовы"
    VERSION = "2.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Настройки сервера
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8001"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
    
    # Пути к файлам
    BASE_DIR = Path(__file__).parent.parent
    UPLOADS_DIR = BASE_DIR / "uploads"
    REPORTS_DIR = BASE_DIR / "reports"
    TEMPLATES_DIR = BASE_DIR / "templates"
    STATIC_DIR = BASE_DIR / "static"
    
    # База данных
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./accounting_assistant.db")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
    USE_OPENAI_FOR_ENHANCEMENT = os.getenv("USE_OPENAI_FOR_ENHANCEMENT", "True").lower() == "true"
    
    # Tesseract
    TESSERACT_PATH = os.getenv("TESSERACT_PATH", "/opt/homebrew/bin/tesseract")
    TESSERACT_LANGUAGES = ["ron", "rus", "eng"]  # Румынский, русский, английский
    
    # Поддерживаемые языки
    SUPPORTED_LANGUAGES = {
        "ro": LanguageConfig(
            code="ro",
            name="Română",
            flag="🇷🇴",
            date_format="%d.%m.%Y",
            currency="MDL",
            currency_symbol="L"
        ),
        "ru": LanguageConfig(
            code="ru", 
            name="Русский",
            flag="🇷🇺",
            date_format="%d.%m.%Y",
            currency="MDL",
            currency_symbol="L"
        )
    }
    
    DEFAULT_LANGUAGE = "ru"
    
    # Типы документов Молдовы
    MOLDOVAN_DOCUMENT_TYPES = [
        DocumentTypeConfig(
            type_id="factura_fiscala",
            name_ro="Factură fiscală",
            name_ru="Счет-фактура",
            keywords_ro=["factură fiscală", "factura fiscală", "fiscal", "tva", "nds"],
            keywords_ru=["счет-фактура", "фактура", "фiscal", "тва", "ндс"],
            required_fields=["number", "date", "seller", "buyer", "idno", "vat_amount", "total_amount"],
            fiscal_code="FISC"
        ),
        DocumentTypeConfig(
            type_id="bon_fiscal",
            name_ro="Bon fiscal",
            name_ru="Фискальный чек",
            keywords_ro=["bon fiscal", "bon", "chitanță", "casă"],
            keywords_ru=["чек", "фискальный чек", "квитанция", "касса"],
            required_fields=["date", "time", "items", "total_amount", "cash_register"],
            fiscal_code="BON"
        ),
        DocumentTypeConfig(
            type_id="stat_plata",
            name_ro="Stat de plată",
            name_ru="Ведомость на выплату",
            keywords_ro=["stat de plată", "salarii", "angajați", "plata"],
            keywords_ru=["ведомость", "зарплата", "сотрудники", "выплата"],
            required_fields=["period", "employees", "positions", "salaries", "total_amount"]
        ),
        DocumentTypeConfig(
            type_id="declaratie_tva",
            name_ro="Declarație TVA",
            name_ru="Декларация НДС",
            keywords_ro=["declarație tva", "tva", "nds", "fiscal"],
            keywords_ru=["декларация ндс", "тва", "ндс", "фiscal"],
            required_fields=["period", "company", "idno", "vat_amount", "total_sales"]
        ),
        DocumentTypeConfig(
            type_id="contract",
            name_ro="Contract",
            name_ru="Договор",
            keywords_ro=["contract", "acord", "convenție"],
            keywords_ru=["договор", "контракт", "соглашение"],
            required_fields=["number", "date", "parties", "subject", "amount", "terms"]
        ),
        DocumentTypeConfig(
            type_id="aviz_expeditie",
            name_ro="Aviz de expediție",
            name_ru="Накладная",
            keywords_ro=["aviz de expediție", "aviz", "expediție", "livrare"],
            keywords_ru=["накладная", "отгрузка", "доставка", "товар"],
            required_fields=["number", "date", "sender", "receiver", "items", "total"]
        ),
        DocumentTypeConfig(
            type_id="ordine_plata",
            name_ro="Ordin de plată",
            name_ru="Платёжное поручение",
            keywords_ro=["ordin de plată", "plată", "transfer", "bancă"],
            keywords_ru=["платёжное поручение", "платёж", "перевод", "банк"],
            required_fields=["number", "date", "payer", "payee", "amount", "purpose"]
        ),
        DocumentTypeConfig(
            type_id="chitanta",
            name_ro="Chitanță",
            name_ru="Квитанция",
            keywords_ro=["chitanță", "primire", "plată", "confirmare"],
            keywords_ru=["квитанция", "получение", "платёж", "подтверждение"],
            required_fields=["number", "date", "payer", "amount", "purpose"]
        )
    ]
    
    # Фискальные коды Молдовы
    FISCAL_CODES = {
        "FISC": "Счет-фактура",
        "BON": "Фискальный чек", 
        "DECL": "Декларация",
        "CONTR": "Договор",
        "AVIZ": "Накладная",
        "ORDIN": "Платёжное поручение",
        "CHIT": "Квитанция"
    }
    
    # Словарь типов документов для шаблонов
    @property
    def DOCUMENT_TYPES(self) -> Dict[str, str]:
        """Возвращает словарь типов документов для использования в шаблонах"""
        return {
            "invoice": "Счет-фактура",
            "receipt": "Чек",
            "contract": "Договор",
            "statement": "Выписка",
            "order": "Заказ",
            "delivery": "Накладная",
            "payment": "Платеж",
            "other": "Другое"
        }
    
    # Настройки экспорта
    EXPORT_FORMATS = ["pdf", "excel", "csv", "json", "xml"]
    REPORT_TEMPLATES = {
        "summary": "Отчёт по всем документам",
        "fiscal": "Фискальный отчёт для FISC",
        "detailed": "Детальный отчёт",
        "custom": "Пользовательский отчёт"
    }
    
    # Настройки уведомлений
    ENABLE_NOTIFICATIONS = True
    NOTIFICATION_TYPES = ["email", "sms", "webhook"]
    
    # Настройки безопасности
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = [".pdf", ".jpg", ".jpeg", ".png", ".tiff", ".bmp"]
    ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".tiff", ".bmp"]
    
    # Настройки OCR
    OCR_CONFIDENCE_THRESHOLD = 0.7
    OCR_TIMEOUT = 30  # секунды
    
    # Настройки классификации
    CLASSIFICATION_CONFIDENCE_THRESHOLD = 0.8
    MAX_KEYWORDS_PER_TYPE = 10
    
    # Настройки отчётов
    REPORT_RETENTION_DAYS = 365
    AUTO_BACKUP_ENABLED = True
    BACKUP_INTERVAL_HOURS = 24
    
    @classmethod
    def validate(cls) -> bool:
        """Проверка валидности конфигурации"""
        try:
            # Проверка обязательных директорий
            for dir_path in [cls.UPLOADS_DIR, cls.REPORTS_DIR, cls.TEMPLATES_DIR, cls.STATIC_DIR]:
                dir_path.mkdir(parents=True, exist_ok=True)
            
            # Проверка OpenAI ключа
            if not cls.OPENAI_API_KEY:
                print("⚠ OpenAI API ключ не настроен. Используется Tesseract OCR.")
            
            # Проверка Tesseract
            import subprocess
            try:
                result = subprocess.run([cls.TESSERACT_PATH, "--version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✓ Tesseract найден: {result.stdout.split()[1]}")
                else:
                    print("⚠ Tesseract не найден или не работает")
                    return False
            except Exception as e:
                print(f"⚠ Ошибка проверки Tesseract: {e}")
                return False
            
            print("✓ Конфигурация валидна")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка конфигурации: {e}")
            return False
    
    @classmethod
    def get_language_config(cls, lang_code: str) -> LanguageConfig:
        """Получение конфигурации языка"""
        return cls.SUPPORTED_LANGUAGES.get(lang_code, cls.SUPPORTED_LANGUAGES[cls.DEFAULT_LANGUAGE])
    
    @classmethod
    def get_document_type_config(cls, type_id: str) -> Optional[DocumentTypeConfig]:
        """Получение конфигурации типа документа"""
        for doc_type in cls.MOLDOVAN_DOCUMENT_TYPES:
            if doc_type.type_id == type_id:
                return doc_type
        return None
    
    @classmethod
    def get_document_type_by_keywords(cls, text: str, lang_code: str = "ru") -> Optional[DocumentTypeConfig]:
        """Определение типа документа по ключевым словам"""
        text_lower = text.lower()
        
        for doc_type in cls.MOLDOVAN_DOCUMENT_TYPES:
            keywords = doc_type.keywords_ro if lang_code == "ro" else doc_type.keywords_ru
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    return doc_type
        
        return None

# Создание экземпляра конфигурации
config = Config() 