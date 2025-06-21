"""
Модуль расширенной обработки документов для бухгалтеров Молдовы
Включает OCR, классификацию, извлечение данных и валидацию
"""

import os
import re
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
from openai import OpenAI
from config import config
from i18n import i18n
from data_models import DocumentData, DocumentField

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Расширенный процессор документов для Молдовы"""
    
    def __init__(self):
        self.tesseract_path = config.TESSERACT_PATH
        self.openai_api_key = config.OPENAI_API_KEY
        self.openai_model = config.OPENAI_MODEL
        self.confidence_threshold = config.OCR_CONFIDENCE_THRESHOLD
        self.classification_threshold = config.CLASSIFICATION_CONFIDENCE_THRESHOLD
        
        # Настройка Tesseract
        if self.tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
        
        # Настройка OpenAI
        self.client = None
        if self.openai_api_key:
            self.client = OpenAI(
                api_key=self.openai_api_key,
                timeout=30.0  # 30 секунд таймаут для запросов
            )
    
    def extract_text_from_image(self, image_path: str, language: str = "ru") -> Tuple[str, float]:
        """Извлечение текста из изображения с помощью Tesseract"""
        try:
            # Определение языков для OCR
            lang_map = {"ru": "rus", "ro": "ron"}
            ocr_lang = lang_map.get(language, "rus+ron+eng")
            
            # Открытие изображения
            image = Image.open(image_path)
            
            # Извлечение текста с настройками для Молдовы
            custom_config = f'--oem 3 --psm 6 -l {ocr_lang}'
            text = pytesseract.image_to_string(image, config=custom_config)
            
            # Получение данных об уверенности
            data = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)
            
            # Расчет средней уверенности
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            logger.info(f"OCR завершен: {len(text)} символов, уверенность: {avg_confidence:.2f}%")
            return text.strip(), avg_confidence / 100.0
            
        except Exception as e:
            logger.error(f"Ошибка OCR: {e}")
            return "", 0.0
    
    def extract_text_from_pdf(self, pdf_path: str, language: str = "ru") -> Tuple[str, float]:
        """Извлечение текста из PDF с поддержкой молдавских документов"""
        try:
            doc = fitz.open(pdf_path)
            text_parts = []
            total_confidence = 0.0
            page_count = 0
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Извлечение текста
                text = page.get_text()
                if text.strip():
                    text_parts.append(text)
                
                # Извлечение изображений для OCR (если текст не найден)
                if not text.strip():
                    image_list = page.get_images()
                    for img_index, img in enumerate(image_list):
                        xref = img[0]
                        pix = fitz.Pixmap(doc, xref)
                        
                        if pix.n - pix.alpha < 4:  # GRAY or RGB
                            img_data = pix.tobytes("png")
                            img_path = f"temp_img_{page_num}_{img_index}.png"
                            
                            with open(img_path, "wb") as f:
                                f.write(img_data)
                            
                            ocr_text, confidence = self.extract_text_from_image(img_path, language)
                            if ocr_text:
                                text_parts.append(ocr_text)
                                total_confidence += confidence
                            
                            os.remove(img_path)
                        pix = None
                
                page_count += 1
                logger.info(f"Обработка страницы {page_num + 1}")
            
            doc.close()
            
            full_text = "\n".join(text_parts)
            avg_confidence = total_confidence / page_count if page_count > 0 else 1.0
            
            logger.info(f"PDF обработка завершена: {len(full_text)} символов, {page_count} страниц")
            return full_text.strip(), avg_confidence
            
        except Exception as e:
            logger.error(f"Ошибка обработки PDF: {e}")
            return "", 0.0
    
    def classify_document(self, text: str, language: str = "ru") -> Tuple[str, float, Dict[str, Any]]:
        """Классификация документа по молдавским типам"""
        try:
            text_lower = text.lower()
            best_match = None
            best_confidence = 0.0
            extracted_data = {}
            
            # Поиск по ключевым словам
            for doc_type in config.MOLDOVAN_DOCUMENT_TYPES:
                keywords = doc_type.keywords_ro if language == "ro" else doc_type.keywords_ru
                matches = 0
                
                for keyword in keywords:
                    if keyword.lower() in text_lower:
                        matches += 1
                
                confidence = matches / len(keywords) if keywords else 0
                
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = doc_type.type_id
                    
                    # Извлечение данных для найденного типа
                    extracted_data = self.extract_document_data(text, doc_type, language)
            
            # Если уверенность ниже порога, используем OpenAI для классификации
            if best_confidence < self.classification_threshold and self.openai_api_key:
                ai_classification = self.classify_with_openai(text, language)
                if ai_classification:
                    best_match = ai_classification.get("type", "unknown")
                    best_confidence = ai_classification.get("confidence", 0.0)
                    extracted_data.update(ai_classification.get("data", {}))
            
            if not best_match:
                best_match = "unknown"
                best_confidence = 1.0
            
            logger.info(f"Документ классифицирован: {best_match} (уверенность: {best_confidence:.2f})")
            return best_match, best_confidence, extracted_data
            
        except Exception as e:
            logger.error(f"Ошибка классификации: {e}")
            return "unknown", 1.0, {}
    
    def extract_document_data(self, text: str, doc_type_config, language: str = "ru") -> Dict[str, Any]:
        """Извлечение данных из документа по типу"""
        data = {}
        text_lines = text.split('\n')
        
        try:
            # Извлечение номера документа
            number_patterns = [
                r'№\s*(\d+)',
                r'Nr\.?\s*(\d+)',
                r'Numărul\s*(\d+)',
                r'Номер\s*(\d+)',
                r'(\d{6,})'  # Длинные номера
            ]
            
            for pattern in number_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    data['number'] = match.group(1)
                    break
            
            # Извлечение даты
            date_patterns = [
                r'(\d{1,2})\.(\d{1,2})\.(\d{4})',
                r'(\d{1,2})/(\d{1,2})/(\d{4})',
                r'(\d{1,2})-(\d{1,2})-(\d{4})'
            ]
            
            for pattern in date_patterns:
                match = re.search(pattern, text)
                if match:
                    day, month, year = match.groups()
                    data['date'] = f"{day.zfill(2)}.{month.zfill(2)}.{year}"
                    break
            
            # Извлечение сумм
            amount_patterns = [
                r'Total[:\s]*([\d\s,\.]+)\s*[Lл]',
                r'Suma[:\s]*([\d\s,\.]+)\s*[Lл]',
                r'Сумма[:\s]*([\d\s,\.]+)\s*[Lл]',
                r'([\d\s,\.]+)\s*[Lл]'
            ]
            
            for pattern in amount_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    amount_str = match.group(1).replace(' ', '').replace(',', '.')
                    try:
                        data['total_amount'] = float(amount_str)
                        break
                    except ValueError:
                        continue
            
            # Извлечение НДС
            vat_patterns = [
                r'TVA[:\s]*([\d\s,\.]+)\s*[Lл]',
                r'НДС[:\s]*([\d\s,\.]+)\s*[Lл]',
                r'(\d+)\s*%'
            ]
            
            for pattern in vat_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    vat_str = match.group(1).replace(' ', '').replace(',', '.')
                    try:
                        data['vat_amount'] = float(vat_str)
                        break
                    except ValueError:
                        continue
            
            # Извлечение IDNO
            idno_patterns = [
                r'IDNO[:\s]*(\d{13})',
                r'Cod fiscal[:\s]*(\d{13})',
                r'Налоговый код[:\s]*(\d{13})'
            ]
            
            for pattern in idno_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    data['idno'] = match.group(1)
                    break
            
            # Извлечение названий компаний
            company_patterns = [
                r'SRL\s+["\']([^"\']+)["\']',
                r'ООО\s+["\']([^"\']+)["\']',
                r'SA\s+["\']([^"\']+)["\']'
            ]
            
            for pattern in company_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    data['company'] = match.group(1).strip()
                    break
            
            logger.info(f"Извлечено данных: {len(data)} полей")
            return data
            
        except Exception as e:
            logger.error(f"Ошибка извлечения данных: {e}")
            return data
    
    def classify_with_openai(self, text: str, language: str = "ru") -> Optional[Dict[str, Any]]:
        """Классификация документа с помощью OpenAI"""
        try:
            if not self.client:
                return None
            
            # Подготовка промпта
            lang_text = "румынском" if language == "ro" else "русском"
            prompt = f"""
            Проанализируй этот документ на {lang_text} языке и определи его тип.
            
            Возможные типы документов:
            - factura_fiscala (счет-фактура)
            - bon_fiscal (фискальный чек)
            - stat_plata (ведомость на выплату)
            - declaratie_tva (декларация НДС)
            - contract (договор)
            - aviz_expeditie (накладная)
            - ordine_plata (платёжное поручение)
            - chitanta (квитанция)
            
            Текст документа:
            {text[:2000]}
            
            Ответь в формате JSON:
            {{
                "type": "тип_документа",
                "confidence": 0.95,
                "data": {{
                    "number": "номер",
                    "date": "дата",
                    "amount": "сумма",
                    "company": "компания"
                }}
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": "Ты эксперт по классификации документов Молдовы."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Проверяем, что ответ не пустой
            if not result_text:
                logger.warning("OpenAI вернул пустой ответ")
                return None
            
            # Проверка, что OpenAI вернул JSON
            if not result_text.startswith("{") or not result_text.endswith("}"):
                logger.warning(f"OpenAI не вернул JSON: {result_text}")
                # Попробуем извлечь JSON из ответа
                match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if match:
                    result_text = match.group(0)
                else:
                    return None

            return json.loads(result_text)
            
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка OpenAI классификации: {e}")
            return None
        except Exception as e:
            logger.error(f"Ошибка OpenAI: {e}")
            return None
    
    def validate_document(self, doc_type: str, extracted_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Валидация документа на основе конфигурации"""
        errors = []
        warnings = []
        
        doc_config = config.get_document_type_config(doc_type)
        if not doc_config:
            warnings.append(f"Конфигурация для типа '{doc_type}' не найдена.")
            return {"errors": errors, "warnings": warnings}
        
        # Проверка обязательных полей
        for field in doc_config.required_fields:
            if field not in extracted_data or not extracted_data[field]:
                errors.append(f"Отсутствует обязательное поле: {i18n.get_text(f'field_{field}')}")
        
        # Специфические проверки
        if "date" in extracted_data and extracted_data["date"]:
            try:
                datetime.strptime(extracted_data["date"], "%d.%m.%Y")
            except (ValueError, TypeError):
                errors.append(f"Неверный формат даты: {extracted_data['date']}")
        
        if "idno" in extracted_data and extracted_data["idno"]:
            if not re.match(r"^\d{13}$", str(extracted_data["idno"])):
                errors.append(f"Неверный формат IDNO: {extracted_data['idno']}")
        
        logger.info(f"Валидация документа: ошибки: {errors}")
        return {"errors": errors, "warnings": warnings}
    
    def process_document(self, file_path: str, language: str = "ru") -> Tuple[Optional[DocumentData], Optional[Dict[str, List[str]]]]:
        """Полная обработка документа: OCR, классификация, извлечение, валидация"""
        try:
            file_ext = Path(file_path).suffix.lower()
            text = ""
            ocr_confidence = 1.0
            
            if file_ext == ".pdf":
                text, ocr_confidence = self.extract_text_from_pdf(file_path, language)
            elif file_ext in config.ALLOWED_IMAGE_EXTENSIONS:
                text, ocr_confidence = self.extract_text_from_image(file_path, language)
            else:
                return None, {"errors": [f"Неподдерживаемый формат файла: {file_ext}"], "warnings": []}

            if not text.strip():
                return None, {"errors": ["Не удалось извлечь текст из документа."], "warnings": []}
            
            # Улучшение текста с помощью OpenAI (опционально)
            if config.USE_OPENAI_FOR_ENHANCEMENT:
                text = self.enhance_text_with_openai(text, language)

            # Классификация
            doc_type, confidence, extracted_data = self.classify_document(text, language)
            
            # Валидация
            validation_result = self.validate_document(doc_type, extracted_data)
            
            # Создание полей
            fields = [DocumentField(name=k, value=str(v)) for k, v in extracted_data.items()]
            
            doc_data = DocumentData(
                doc_type=doc_type,
                confidence=confidence,
                raw_text=text,
                fields=fields
            )
            
            logger.info(f"Обработка завершена: {doc_type} (уверенность: {confidence:.2f})")
            return doc_data, validation_result

        except Exception as e:
            logger.error(f"Ошибка обработки документа: {e}", exc_info=True)
            return None, {"errors": [f"Внутренняя ошибка сервера: {e}"], "warnings": []}

    def enhance_text_with_openai(self, text: str, language: str = "ru") -> str:
        """Улучшение и структурирование текста с помощью OpenAI"""
        try:
            if not self.client:
                return text
            
            lang_text = "румынском" if language == "ro" else "русском"
            prompt = f"""
            Приведи в порядок и структурируй следующий текст, извлеченный из бухгалтерского документа на {lang_text} языке.
            Исправь ошибки OCR, сохрани ключевую информацию, такую как даты, номера, суммы, названия компаний.
            
            Оригинальный текст:
            {text[:3000]}
            
            Улучшенный текст:
            """
            
            response = self.client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": "Ты ассистент, который помогает исправлять текст после OCR."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.2
            )
            
            enhanced_text = response.choices[0].message.content.strip()
            logger.info("Текст улучшен с помощью OpenAI")
            return enhanced_text
            
        except Exception as e:
            logger.error(f"Ошибка улучшения текста: {e}")
            return text

# Создаем единственный экземпляр процессора
document_processor = DocumentProcessor()