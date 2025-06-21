"""
Модуль интернационализации для AI Помощник Бухгалтера Молдовы
Поддерживает русский и румынский языки
"""

from typing import Dict, Any, Optional
from config import config

class I18nManager:
    """Менеджер интернационализации"""
    
    # Переводы для русского языка
    TRANSLATIONS_RU = {
        # Общие элементы
        "app_name": "AI Помощник Бухгалтера Молдовы",
        "loading": "Загрузка...",
        "error": "Ошибка",
        "success": "Успешно",
        "cancel": "Отмена",
        "save": "Сохранить",
        "delete": "Удалить",
        "edit": "Редактировать",
        "view": "Просмотр",
        "search": "Поиск",
        "filter": "Фильтр",
        "export": "Экспорт",
        "import": "Импорт",
        "back": "Назад",
        "next": "Далее",
        "submit": "Отправить",
        "close": "Закрыть",
        "yes": "Да",
        "no": "Нет",
        "confirm": "Подтвердить",
        
        # Навигация
        "dashboard": "Главная",
        "documents": "Документы",
        "reports": "Отчёты",
        "settings": "Настройки",
        "help": "Помощь",
        "about": "О программе",
        
        # Документы
        "upload_document": "Загрузить документ",
        "document_processing": "Обработка документа",
        "document_classification": "Классификация документа",
        "document_type": "Тип документа",
        "document_date": "Дата документа",
        "document_number": "Номер документа",
        "document_amount": "Сумма документа",
        "document_status": "Статус документа",
        "document_confidence": "Уверенность",
        "document_processing_complete": "Обработка завершена",
        "document_processing_failed": "Ошибка обработки",
        
        # Типы документов
        "factura_fiscala": "Счет-фактура",
        "bon_fiscal": "Фискальный чек",
        "stat_plata": "Ведомость на выплату",
        "declaratie_tva": "Декларация НДС",
        "contract": "Договор",
        "aviz_expeditie": "Накладная",
        "ordine_plata": "Платёжное поручение",
        "chitanta": "Квитанция",
        "unknown": "Неизвестный тип",
        
        # Поля документов
        "number": "Номер",
        "date": "Дата",
        "seller": "Продавец",
        "buyer": "Покупатель",
        "idno": "IDNO",
        "vat_amount": "Сумма НДС",
        "total_amount": "Общая сумма",
        "time": "Время",
        "items": "Товары",
        "cash_register": "Касса",
        "period": "Период",
        "employees": "Сотрудники",
        "positions": "Должности",
        "salaries": "Зарплаты",
        "company": "Компания",
        "total_sales": "Общие продажи",
        "parties": "Стороны",
        "subject": "Предмет",
        "amount": "Сумма",
        "terms": "Условия",
        "sender": "Отправитель",
        "receiver": "Получатель",
        "total": "Итого",
        "payer": "Плательщик",
        "payee": "Получатель платежа",
        "purpose": "Назначение платежа",
        
        # Отчёты
        "reports": "Отчёты",
        "summary_report": "Сводный отчёт",
        "fiscal_report": "Фискальный отчёт",
        "detailed_report": "Детальный отчёт",
        "custom_report": "Пользовательский отчёт",
        "generate_report": "Сгенерировать отчёт",
        "export_report": "Экспортировать отчёт",
        "report_period": "Период отчёта",
        "report_type": "Тип отчёта",
        "report_format": "Формат отчёта",
        "report_generated": "Отчёт сгенерирован",
        "report_exported": "Отчёт экспортирован",
        
        # Статистика
        "total_documents": "Всего документов",
        "documents_this_month": "Документов за месяц",
        "total_amount_processed": "Общая сумма обработана",
        "vat_total": "Общая сумма НДС",
        "documents_by_type": "Документы по типам",
        "processing_statistics": "Статистика обработки",
        
        # Настройки
        "language": "Язык",
        "language_ru": "Русский",
        "language_ro": "Română",
        "currency": "Валюта",
        "date_format": "Формат даты",
        "notifications": "Уведомления",
        "email_notifications": "Email уведомления",
        "sms_notifications": "SMS уведомления",
        "auto_backup": "Автоматическое резервное копирование",
        "ocr_settings": "Настройки OCR",
        "classification_settings": "Настройки классификации",
        
        # Уведомления
        "notification_success": "Операция выполнена успешно",
        "notification_error": "Произошла ошибка",
        "notification_warning": "Предупреждение",
        "notification_info": "Информация",
        
        # Ошибки
        "error_file_too_large": "Файл слишком большой",
        "error_invalid_format": "Неподдерживаемый формат файла",
        "error_processing_failed": "Ошибка обработки документа",
        "error_ocr_failed": "Ошибка OCR",
        "error_classification_failed": "Ошибка классификации",
        "error_database": "Ошибка базы данных",
        "error_network": "Ошибка сети",
        "error_unauthorized": "Неавторизованный доступ",
        "error_not_found": "Не найдено",
        
        # Сообщения
        "message_upload_success": "Документ успешно загружен",
        "message_processing_started": "Обработка документа началась",
        "message_processing_complete": "Обработка документа завершена",
        "message_document_saved": "Документ сохранён",
        "message_document_deleted": "Документ удалён",
        "message_report_generated": "Отчёт сгенерирован",
        "message_settings_saved": "Настройки сохранены",
        
        # Подсказки
        "hint_drag_drop": "Перетащите файлы сюда или нажмите для выбора",
        "hint_supported_formats": "Поддерживаемые форматы: PDF, JPG, PNG, TIFF",
        "hint_max_file_size": "Максимальный размер файла: 50MB",
        "hint_search_documents": "Поиск по номеру, дате, типу документа",
        "hint_filter_documents": "Фильтр по периоду, типу, статусу",
        
        # Валидация
        "validation_required": "Это поле обязательно",
        "validation_invalid_date": "Неверный формат даты",
        "validation_invalid_number": "Неверный формат числа",
        "validation_invalid_email": "Неверный формат email",
        "validation_file_required": "Выберите файл",
        "validation_file_size": "Размер файла превышает лимит",
        "validation_file_format": "Неподдерживаемый формат файла",
        
        # Фискальные коды
        "fiscal_code_fisc": "Счет-фактура",
        "fiscal_code_bon": "Фискальный чек",
        "fiscal_code_decl": "Декларация",
        "fiscal_code_contr": "Договор",
        "fiscal_code_aviz": "Накладная",
        "fiscal_code_ordin": "Платёжное поручение",
        "fiscal_code_chit": "Квитанция",
        
        # Валюты
        "currency_mdl": "Молдавский лей",
        "currency_symbol_l": "L",
        
        # Форматы дат
        "date_format_ddmmyyyy": "ДД.ММ.ГГГГ",
        
        # Статусы
        "status_processing": "Обрабатывается",
        "status_completed": "Завершено",
        "status_failed": "Ошибка",
        "status_pending": "Ожидает",
        "status_archived": "Архивировано",
        
        # Уровни уверенности
        "confidence_high": "Высокая",
        "confidence_medium": "Средняя",
        "confidence_low": "Низкая",
        "confidence_unknown": "Неизвестно",
        
        # Действия
        "action_view": "Просмотр",
        "action_edit": "Редактировать",
        "action_delete": "Удалить",
        "action_download": "Скачать",
        "action_print": "Печать",
        "action_share": "Поделиться",
        "action_archive": "Архивировать",
        "action_restore": "Восстановить",
        
        # Меню
        "menu_dashboard": "Главная панель",
        "menu_documents": "Документы",
        "menu_upload": "Загрузка",
        "menu_search": "Поиск",
        "menu_reports": "Отчёты",
        "menu_statistics": "Статистика",
        "menu_settings": "Настройки",
        "menu_help": "Помощь",
        "menu_about": "О программе",
        
        # Заголовки страниц
        "page_title_dashboard": "Главная панель - AI Помощник Бухгалтера",
        "page_title_documents": "Документы - AI Помощник Бухгалтера",
        "page_title_upload": "Загрузка документов - AI Помощник Бухгалтера",
        "page_title_reports": "Отчёты - AI Помощник Бухгалтера",
        "page_title_settings": "Настройки - AI Помощник Бухгалтера",
        
        # Описания
        "description_dashboard": "Главная панель управления документами и отчётами",
        "description_documents": "Управление и просмотр всех документов",
        "description_upload": "Загрузка и обработка новых документов",
        "description_reports": "Генерация и экспорт отчётов",
        "description_settings": "Настройки приложения и пользователя",
        
        # Помощь
        "help_upload": "Как загружать документы",
        "help_classification": "Как работает классификация",
        "help_reports": "Как создавать отчёты",
        "help_settings": "Как настроить приложение",
        "help_support": "Получить поддержку",
        
        # О программе
        "about_version": "Версия",
        "about_developer": "Разработчик",
        "about_license": "Лицензия",
        "about_contact": "Контакты",
        "about_description": "Интеллектуальный помощник для бухгалтеров Молдовы"
    }
    
    # Переводы для румынского языка
    TRANSLATIONS_RO = {
        # Общие элементы
        "app_name": "AI Asistent Contabil Moldova",
        "loading": "Se încarcă...",
        "error": "Eroare",
        "success": "Succes",
        "cancel": "Anulare",
        "save": "Salvare",
        "delete": "Ștergere",
        "edit": "Editare",
        "view": "Vizualizare",
        "search": "Căutare",
        "filter": "Filtru",
        "export": "Export",
        "import": "Import",
        "back": "Înapoi",
        "next": "Următorul",
        "submit": "Trimite",
        "close": "Închide",
        "yes": "Da",
        "no": "Nu",
        "confirm": "Confirmă",
        
        # Навигация
        "dashboard": "Principal",
        "documents": "Documente",
        "reports": "Rapoarte",
        "settings": "Setări",
        "help": "Ajutor",
        "about": "Despre",
        
        # Документы
        "upload_document": "Încarcă document",
        "document_processing": "Procesarea documentului",
        "document_classification": "Clasificarea documentului",
        "document_type": "Tipul documentului",
        "document_date": "Data documentului",
        "document_number": "Numărul documentului",
        "document_amount": "Suma documentului",
        "document_status": "Statusul documentului",
        "document_confidence": "Încredere",
        "document_processing_complete": "Procesarea finalizată",
        "document_processing_failed": "Eroare la procesare",
        
        # Типы документов
        "factura_fiscala": "Factură fiscală",
        "bon_fiscal": "Bon fiscal",
        "stat_plata": "Stat de plată",
        "declaratie_tva": "Declarație TVA",
        "contract": "Contract",
        "aviz_expeditie": "Aviz de expediție",
        "ordine_plata": "Ordin de plată",
        "chitanta": "Chitanță",
        "unknown": "Tip necunoscut",
        
        # Поля документов
        "number": "Număr",
        "date": "Data",
        "seller": "Vânzător",
        "buyer": "Cumpărător",
        "idno": "IDNO",
        "vat_amount": "Suma TVA",
        "total_amount": "Suma totală",
        "time": "Ora",
        "items": "Articole",
        "cash_register": "Casă",
        "period": "Perioada",
        "employees": "Angajați",
        "positions": "Poziții",
        "salaries": "Salarii",
        "company": "Companie",
        "total_sales": "Vânzări totale",
        "parties": "Părți",
        "subject": "Subiect",
        "amount": "Suma",
        "terms": "Termeni",
        "sender": "Expeditor",
        "receiver": "Destinatar",
        "total": "Total",
        "payer": "Plătitor",
        "payee": "Beneficiar",
        "purpose": "Scopul plății",
        
        # Отчёты
        "reports": "Rapoarte",
        "summary_report": "Raport sumar",
        "fiscal_report": "Raport fiscal",
        "detailed_report": "Raport detaliat",
        "custom_report": "Raport personalizat",
        "generate_report": "Generează raport",
        "export_report": "Exportă raport",
        "report_period": "Perioada raportului",
        "report_type": "Tipul raportului",
        "report_format": "Formatul raportului",
        "report_generated": "Raportul generat",
        "report_exported": "Raportul exportat",
        
        # Статистика
        "total_documents": "Total documente",
        "documents_this_month": "Documente luna aceasta",
        "total_amount_processed": "Suma totală procesată",
        "vat_total": "Total TVA",
        "documents_by_type": "Documente pe tipuri",
        "processing_statistics": "Statistici procesare",
        
        # Настройки
        "language": "Limba",
        "language_ru": "Русский",
        "language_ro": "Română",
        "currency": "Moneda",
        "date_format": "Formatul datei",
        "notifications": "Notificări",
        "email_notifications": "Notificări email",
        "sms_notifications": "Notificări SMS",
        "auto_backup": "Backup automat",
        "ocr_settings": "Setări OCR",
        "classification_settings": "Setări clasificare",
        
        # Уведомления
        "notification_success": "Operația finalizată cu succes",
        "notification_error": "A apărut o eroare",
        "notification_warning": "Avertisment",
        "notification_info": "Informație",
        
        # Ошибки
        "error_file_too_large": "Fișierul este prea mare",
        "error_invalid_format": "Format de fișier nesuportat",
        "error_processing_failed": "Eroare la procesarea documentului",
        "error_ocr_failed": "Eroare OCR",
        "error_classification_failed": "Eroare la clasificare",
        "error_database": "Eroare bază de date",
        "error_network": "Eroare rețea",
        "error_unauthorized": "Acces neautorizat",
        "error_not_found": "Nu a fost găsit",
        
        # Сообщения
        "message_upload_success": "Documentul încărcat cu succes",
        "message_processing_started": "Procesarea documentului a început",
        "message_processing_complete": "Procesarea documentului finalizată",
        "message_document_saved": "Documentul salvat",
        "message_document_deleted": "Documentul șters",
        "message_report_generated": "Raportul generat",
        "message_settings_saved": "Setările salvate",
        
        # Подсказки
        "hint_drag_drop": "Trageți fișierele aici sau faceți clic pentru a selecta",
        "hint_supported_formats": "Formate suportate: PDF, JPG, PNG, TIFF",
        "hint_max_file_size": "Dimensiunea maximă a fișierului: 50MB",
        "hint_search_documents": "Căutare după număr, dată, tip document",
        "hint_filter_documents": "Filtru după perioadă, tip, status",
        
        # Валидация
        "validation_required": "Acest câmp este obligatoriu",
        "validation_invalid_date": "Format de dată invalid",
        "validation_invalid_number": "Format de număr invalid",
        "validation_invalid_email": "Format de email invalid",
        "validation_file_required": "Selectați un fișier",
        "validation_file_size": "Dimensiunea fișierului depășește limita",
        "validation_file_format": "Format de fișier nesuportat",
        
        # Фискальные коды
        "fiscal_code_fisc": "Factură fiscală",
        "fiscal_code_bon": "Bon fiscal",
        "fiscal_code_decl": "Declarație",
        "fiscal_code_contr": "Contract",
        "fiscal_code_aviz": "Aviz",
        "fiscal_code_ordin": "Ordin de plată",
        "fiscal_code_chit": "Chitanță",
        
        # Валюты
        "currency_mdl": "Leu moldovenesc",
        "currency_symbol_l": "L",
        
        # Форматы дат
        "date_format_ddmmyyyy": "ZZ.LL.AAAA",
        
        # Статусы
        "status_processing": "Se procesează",
        "status_completed": "Finalizat",
        "status_failed": "Eroare",
        "status_pending": "În așteptare",
        "status_archived": "Arhivat",
        
        # Уровни уверенности
        "confidence_high": "Ridicată",
        "confidence_medium": "Medie",
        "confidence_low": "Scăzută",
        "confidence_unknown": "Necunoscută",
        
        # Действия
        "action_view": "Vizualizare",
        "action_edit": "Editare",
        "action_delete": "Ștergere",
        "action_download": "Descărcare",
        "action_print": "Tipărire",
        "action_share": "Partajare",
        "action_archive": "Arhivare",
        "action_restore": "Restaurare",
        
        # Меню
        "menu_dashboard": "Panou principal",
        "menu_documents": "Documente",
        "menu_upload": "Încărcare",
        "menu_search": "Căutare",
        "menu_reports": "Rapoarte",
        "menu_statistics": "Statistici",
        "menu_settings": "Setări",
        "menu_help": "Ajutor",
        "menu_about": "Despre",
        
        # Заголовки страниц
        "page_title_dashboard": "Panou principal - AI Asistent Contabil",
        "page_title_documents": "Documente - AI Asistent Contabil",
        "page_title_upload": "Încărcare documente - AI Asistent Contabil",
        "page_title_reports": "Rapoarte - AI Asistent Contabil",
        "page_title_settings": "Setări - AI Asistent Contabil",
        
        # Описания
        "description_dashboard": "Panou principal pentru gestionarea documentelor și rapoartelor",
        "description_documents": "Gestionarea și vizualizarea tuturor documentelor",
        "description_upload": "Încărcarea și procesarea documentelor noi",
        "description_reports": "Generarea și exportul rapoartelor",
        "description_settings": "Setările aplicației și ale utilizatorului",
        
        # Помощь
        "help_upload": "Cum să încărci documente",
        "help_classification": "Cum funcționează clasificarea",
        "help_reports": "Cum să creezi rapoarte",
        "help_settings": "Cum să configurezi aplicația",
        "help_support": "Obține suport",
        
        # О программе
        "about_version": "Versiunea",
        "about_developer": "Dezvoltator",
        "about_license": "Licență",
        "about_contact": "Contacte",
        "about_description": "Asistent inteligent pentru contabilii din Moldova"
    }
    
    def __init__(self, default_language: str = "ru"):
        self.default_language = default_language
        self.current_language = default_language
        self.translations = {
            "ru": self.TRANSLATIONS_RU,
            "ro": self.TRANSLATIONS_RO
        }
    
    def set_language(self, language: str) -> None:
        """Установка текущего языка"""
        if language in self.translations:
            self.current_language = language
    
    def get_text(self, key: str, language: Optional[str] = None) -> str:
        """Получение перевода по ключу"""
        lang = language or self.current_language
        translations = self.translations.get(lang, self.translations[self.default_language])
        return translations.get(key, key)
    
    def get_text_ro(self, key: str) -> str:
        """Получение перевода на румынском языке"""
        return self.get_text(key, "ro")
    
    def get_text_ru(self, key: str) -> str:
        """Получение перевода на русском языке"""
        return self.get_text(key, "ru")
    
    def get_document_type_name(self, type_id: str, language: Optional[str] = None) -> str:
        """Получение названия типа документа"""
        return self.get_text(type_id, language)
    
    def get_fiscal_code_name(self, code: str, language: Optional[str] = None) -> str:
        """Получение названия фискального кода"""
        return self.get_text(f"fiscal_code_{code.lower()}", language)
    
    def get_currency_name(self, currency: str, language: Optional[str] = None) -> str:
        """Получение названия валюты"""
        return self.get_text(f"currency_{currency.lower()}", language)
    
    def get_currency_symbol(self, currency: str) -> str:
        """Получение символа валюты"""
        return self.get_text(f"currency_symbol_{currency.lower()}")
    
    def get_date_format(self, language: Optional[str] = None) -> str:
        """Получение формата даты для языка"""
        return self.get_text("date_format_ddmmyyyy", language)
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Получение списка поддерживаемых языков"""
        return {
            "ru": self.get_text("language_ru", "ru"),
            "ro": self.get_text("language_ro", "ro")
        }
    
    def format_currency(self, amount: float, currency: str = "MDL", language: Optional[str] = None) -> str:
        """Форматирование валюты"""
        symbol = self.get_currency_symbol(currency)
        lang = language or self.current_language
        
        if lang == "ro":
            return f"{amount:.2f} {symbol}"
        else:
            return f"{amount:.2f} {symbol}"
    
    def format_date(self, date_obj, language: Optional[str] = None) -> str:
        """Форматирование даты"""
        lang = language or self.current_language
        format_str = self.get_date_format(lang)
        return date_obj.strftime(format_str)
    
    def get_validation_message(self, field: str, error_type: str, language: Optional[str] = None) -> str:
        """Получение сообщения валидации"""
        key = f"validation_{error_type}"
        return self.get_text(key, language)
    
    def get_error_message(self, error_type: str, language: Optional[str] = None) -> str:
        """Получение сообщения об ошибке"""
        key = f"error_{error_type}"
        return self.get_text(key, language)
    
    def get_success_message(self, action: str, language: Optional[str] = None) -> str:
        """Получение сообщения об успехе"""
        key = f"message_{action}_success"
        return self.get_text(key, language)
    
    def get_all_translations(self, language: str) -> Dict[str, str]:
        """Получение всех переводов для языка"""
        return self.translations.get(language, {})

# Создание глобального экземпляра
i18n = I18nManager(config.DEFAULT_LANGUAGE) 