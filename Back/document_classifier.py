import re
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class DocumentField:
    """Поле документа с извлеченным значением"""
    name: str
    value: str
    confidence: float = 1.0

@dataclass
class DocumentData:
    """Структура данных документа"""
    doc_type: str
    fields: List[DocumentField]
    raw_text: str
    confidence: float = 1.0

class MoldovanDocumentClassifier:
    """Классификатор молдавских документов"""
    
    def __init__(self):
        # Ключевые слова для определения типа документа
        self.doc_type_keywords = {
            "factura_fiscala": [
                "factură fiscală", "factura fiscala", "invoice", "счет-фактура",
                "fiscal", "tva", "nds", "idno", "cod fiscal"
            ],
            "bon_fiscal": [
                "bon fiscal", "bon", "чек", "receipt", "кассовый чек",
                "terminal fiscal", "fiscal terminal"
            ],
            "stat_plata": [
                "stat de plată", "stat plata", "ведомость", "зарплата",
                "salary", "wage", "employee", "сотрудник", "зарплата"
            ],
            "act_achizitie": [
                "act de achiziție", "act achizitie", "акт покупки",
                "purchase act", "автомобиль", "машина", "auto"
            ],
            "ordin_plata": [
                "ordin de plată", "ordin plata", "платежное поручение",
                "payment order", "банк", "bank", "iban"
            ],
            "raport_avans": [
                "raport de avans", "raport avans", "отчет аванса",
                "advance report", "командировка", "business trip"
            ]
        }
        
        # Паттерны для извлечения полей
        self.field_patterns = {
            "factura_fiscala": {
                "number": r"(?:factură|factura|invoice|счет)[\s\-\#]*[№\#]?\s*([A-Z0-9\-]+)",
                "date": r"(?:data|дата|date)[\s:]*(\d{1,2}[\.\/\-]\d{1,2}[\.\/\-]\d{2,4})",
                "seller": r"(?:furnizor|поставщик|seller)[\s:]*([^\n]+)",
                "buyer": r"(?:client|cumpărător|покупатель|buyer)[\s:]*([^\n]+)",
                "idno": r"(?:idno|cod fiscal|идентификационный номер)[\s:]*([0-9]{13})",
                "vat_amount": r"(?:tva|nds|ндс)[\s:]*([0-9,\.]+)",
                "total_amount": r"(?:total|итого|suma totala)[\s:]*([0-9,\.]+)"
            },
            "bon_fiscal": {
                "items": r"([^\n]+)\s+([0-9,\.]+)\s+([0-9,\.]+)",
                "quantity": r"(?:cantitate|количество|qty)[\s:]*([0-9,\.]+)",
                "total_amount": r"(?:total|итого|suma totala)[\s:]*([0-9,\.]+)",
                "cash_register": r"(?:terminal|касса|cash)[\s:]*([A-Z0-9\-]+)"
            },
            "stat_plata": {
                "employee": r"([А-Яа-яA-Za-z\s]+)\s+([А-Яа-яA-Za-z\s]+)",
                "position": r"(?:должность|position)[\s:]*([^\n]+)",
                "salary": r"(?:зарплата|salary)[\s:]*([0-9,\.]+)",
                "taxes": r"(?:налоги|taxes)[\s:]*([0-9,\.]+)",
                "contributions": r"(?:взносы|contributions)[\s:]*([0-9,\.]+)"
            },
            "act_achizitie": {
                "car_data": r"(?:автомобиль|машина|auto)[\s:]*([^\n]+)",
                "amount": r"(?:сумма|amount)[\s:]*([0-9,\.]+)",
                "buyer": r"(?:покупатель|buyer)[\s:]*([^\n]+)",
                "seller": r"(?:продавец|seller)[\s:]*([^\n]+)"
            },
            "ordin_plata": {
                "amount": r"(?:сумма|amount)[\s:]*([0-9,\.]+)",
                "purpose": r"(?:назначение|purpose)[\s:]*([^\n]+)",
                "bank": r"(?:банк|bank)[\s:]*([^\n]+)",
                "iban": r"(?:iban)[\s:]*([A-Z]{2}[0-9]{2}[A-Z0-9]{4}[0-9]{7})"
            },
            "raport_avans": {
                "amount": r"(?:сумма|amount)[\s:]*([0-9,\.]+)",
                "date": r"(?:дата|date)[\s:]*(\d{1,2}[\.\/\-]\d{1,2}[\.\/\-]\d{2,4})",
                "business_trip": r"(?:командировка|business trip)[\s:]*([^\n]+)",
                "spent": r"(?:потрачено|spent)[\s:]*([0-9,\.]+)",
                "remaining": r"(?:остаток|remaining)[\s:]*([0-9,\.]+)"
            }
        }
    
    def classify_document(self, text: str) -> str:
        """Определяет тип документа на основе текста"""
        text_lower = text.lower()
        
        # Подсчитываем совпадения для каждого типа документа
        doc_scores = {}
        for doc_type, keywords in self.doc_type_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    score += 1
            doc_scores[doc_type] = score
        
        # Возвращаем тип с наибольшим количеством совпадений
        if doc_scores:
            best_type = max(doc_scores, key=doc_scores.get)
            if doc_scores[best_type] > 0:
                logger.info(f"Определен тип документа: {best_type} (счет: {doc_scores[best_type]})")
                return best_type
        
        logger.warning("Тип документа не определен")
        return "unknown"
    
    def extract_fields(self, text: str, doc_type: str) -> List[DocumentField]:
        """Извлекает поля из документа определенного типа"""
        fields = []
        
        if doc_type not in self.field_patterns:
            logger.warning(f"Паттерны для типа документа {doc_type} не найдены")
            return fields
        
        patterns = self.field_patterns[doc_type]
        
        for field_name, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                # Берем первое совпадение
                value = matches[0] if isinstance(matches[0], str) else " ".join(matches[0])
                fields.append(DocumentField(
                    name=field_name,
                    value=value.strip(),
                    confidence=0.8
                ))
                logger.info(f"Извлечено поле {field_name}: {value}")
        
        return fields
    
    def validate_document(self, doc_data: DocumentData) -> Dict[str, List[str]]:
        """Проверяет документ на ошибки и несоответствия"""
        errors = []
        warnings = []
        
        # Проверка IDNO (13 цифр)
        idno_field = next((f for f in doc_data.fields if f.name == "idno"), None)
        if idno_field:
            if not re.match(r"^[0-9]{13}$", idno_field.value):
                errors.append(f"Неверный формат IDNO: {idno_field.value} (должно быть 13 цифр)")
        
        # Проверка дат
        date_fields = [f for f in doc_data.fields if f.name == "date"]
        for date_field in date_fields:
            try:
                # Пробуем разные форматы дат
                for fmt in ["%d.%m.%Y", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%y", "%d/%m/%y"]:
                    try:
                        parsed_date = datetime.strptime(date_field.value, fmt)
                        if parsed_date.year > 2030 or parsed_date.year < 2000:
                            warnings.append(f"Подозрительная дата: {date_field.value}")
                        break
                    except ValueError:
                        continue
                else:
                    errors.append(f"Неверный формат даты: {date_field.value}")
            except Exception:
                errors.append(f"Ошибка парсинга даты: {date_field.value}")
        
        # Проверка сумм
        amount_fields = [f for f in doc_data.fields if "amount" in f.name]
        for amount_field in amount_fields:
            try:
                amount = float(amount_field.value.replace(",", ""))
                if amount <= 0:
                    errors.append(f"Некорректная сумма: {amount_field.value}")
            except ValueError:
                errors.append(f"Неверный формат суммы: {amount_field.value}")
        
        # Проверка НДС (20%)
        vat_field = next((f for f in doc_data.fields if f.name == "vat_amount"), None)
        if vat_field and doc_data.doc_type == "factura_fiscala":
            try:
                vat_amount = float(vat_field.value.replace(",", ""))
                total_field = next((f for f in doc_data.fields if f.name == "total_amount"), None)
                if total_field:
                    total_amount = float(total_field.value.replace(",", ""))
                    expected_vat = total_amount * 0.2
                    if abs(vat_amount - expected_vat) > 0.01:
                        warnings.append(f"НДС не соответствует 20%: {vat_amount} (ожидалось {expected_vat:.2f})")
            except ValueError:
                errors.append(f"Неверный формат НДС: {vat_field.value}")
        
        return {"errors": errors, "warnings": warnings}
    
    def process_document(self, text: str) -> DocumentData:
        """Полная обработка документа: классификация, извлечение полей и валидация"""
        logger.info("Начинаем обработку документа")
        
        # Классификация
        doc_type = self.classify_document(text)
        
        # Извлечение полей
        fields = self.extract_fields(text, doc_type)
        
        # Создание структуры данных
        doc_data = DocumentData(
            doc_type=doc_type,
            fields=fields,
            raw_text=text
        )
        
        # Валидация
        validation_result = self.validate_document(doc_data)
        
        # Добавляем результаты валидации в логи
        if validation_result["errors"]:
            logger.error(f"Ошибки в документе: {validation_result['errors']}")
        if validation_result["warnings"]:
            logger.warning(f"Предупреждения в документе: {validation_result['warnings']}")
        
        return doc_data 