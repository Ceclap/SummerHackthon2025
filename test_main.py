"""
Тесты для AI Помощника Бухгалтера
"""

import pytest
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from PIL import Image
import io

from main import (
    validate_file, 
    extract_text_from_image, 
    extract_text_from_pdf, 
    classify_document
)
from config import config


class TestFileValidation:
    """Тесты для валидации файлов"""
    
    def test_valid_file_extension(self):
        """Тест валидного расширения файла"""
        mock_file = Mock()
        mock_file.filename = "test.pdf"
        
        # Не должно вызывать исключение
        validate_file(mock_file)
    
    def test_invalid_file_extension(self):
        """Тест невалидного расширения файла"""
        from fastapi import HTTPException
        
        mock_file = Mock()
        mock_file.filename = "test.txt"
        
        with pytest.raises(HTTPException) as exc_info:
            validate_file(mock_file)
        
        assert exc_info.value.status_code == 400
        assert "Неподдерживаемый формат файла" in str(exc_info.value.detail)
    
    def test_empty_filename(self):
        """Тест пустого имени файла"""
        from fastapi import HTTPException
        
        mock_file = Mock()
        mock_file.filename = None
        
        with pytest.raises(HTTPException) as exc_info:
            validate_file(mock_file)
        
        assert exc_info.value.status_code == 400
        assert "Файл не выбран" in str(exc_info.value.detail)


class TestTextExtraction:
    """Тесты для извлечения текста"""
    
    @patch('main.pytesseract.image_to_string')
    def test_extract_text_from_image_success(self, mock_ocr):
        """Тест успешного извлечения текста из изображения"""
        mock_ocr.return_value = "Test text from image"
        
        # Создаем временное изображение
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            # Создаем простое изображение
            img = Image.new('RGB', (100, 100), color='white')
            img.save(tmp_file.name)
            
            try:
                result = extract_text_from_image(tmp_file.name)
                assert result == "Test text from image"
                mock_ocr.assert_called_once()
            finally:
                os.unlink(tmp_file.name)
    
    @patch('main.pytesseract.image_to_string')
    def test_extract_text_from_image_error(self, mock_ocr):
        """Тест ошибки при извлечении текста из изображения"""
        from fastapi import HTTPException
        
        mock_ocr.side_effect = Exception("OCR error")
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            img = Image.new('RGB', (100, 100), color='white')
            img.save(tmp_file.name)
            
            try:
                with pytest.raises(HTTPException) as exc_info:
                    extract_text_from_image(tmp_file.name)
                
                assert exc_info.value.status_code == 500
                assert "Ошибка при обработке изображения" in str(exc_info.value.detail)
            finally:
                os.unlink(tmp_file.name)
    
    @patch('main.fitz.open')
    def test_extract_text_from_pdf_success(self, mock_fitz_open):
        """Тест успешного извлечения текста из PDF"""
        # Мокаем PDF документ
        mock_doc = Mock()
        mock_page = Mock()
        mock_page.get_text.return_value = "Test text from PDF"
        mock_doc.__iter__.return_value = [mock_page]
        mock_fitz_open.return_value = mock_doc
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            try:
                result = extract_text_from_pdf(tmp_file.name)
                assert "Test text from PDF" in result
                mock_doc.close.assert_called_once()
            finally:
                os.unlink(tmp_file.name)
    
    @patch('main.fitz.open')
    def test_extract_text_from_pdf_error(self, mock_fitz_open):
        """Тест ошибки при извлечении текста из PDF"""
        from fastapi import HTTPException
        
        mock_fitz_open.side_effect = Exception("PDF error")
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            try:
                with pytest.raises(HTTPException) as exc_info:
                    extract_text_from_pdf(tmp_file.name)
                
                assert exc_info.value.status_code == 500
                assert "Ошибка при обработке PDF" in str(exc_info.value.detail)
            finally:
                os.unlink(tmp_file.name)


class TestDocumentClassification:
    """Тесты для классификации документов"""
    
    def test_fiscal_document_classification(self):
        """Тест классификации налогового документа"""
        text = """
        Serviciul Fiscal de Stat
        Declarația anuală de impozit
        TVA deductibil și colectat
        """
        
        result = classify_document(text)
        
        assert result["type"] == "Serviciul Fiscal de Stat (Налоговая служба)"
        assert result["confidence"] > 0
    
    def test_asp_document_classification(self):
        """Тест классификации документа ASP"""
        text = """
        Agenția Servicii Publice
        Certificat de înregistrare
        Persoană juridică
        """
        
        result = classify_document(text)
        
        assert result["type"] == "Agenția Servicii Publice (Агентство гос. услуг)"
        assert result["confidence"] > 0
    
    def test_contract_classification(self):
        """Тест классификации контракта"""
        text = """
        Contract de prestări servicii
        Semnat între părți
        Valoare totală
        """
        
        result = classify_document(text)
        
        assert result["type"] == "Contract/Соглашение"
        assert result["confidence"] > 0
    
    def test_invoice_classification(self):
        """Тест классификации счета"""
        text = """
        Factură nr. 001/2024
        Client: Test SRL
        Sumă totală cu TVA
        """
        
        result = classify_document(text)
        
        assert result["type"] == "Factură/Счет"
        assert result["confidence"] > 0
    
    def test_unknown_document_classification(self):
        """Тест классификации неизвестного документа"""
        text = """
        Acest text nu conține cuvinte cheie
        pentru clasificarea documentelor
        """
        
        result = classify_document(text)
        
        assert result["type"] == "Не удалось определить тип документа"
        assert result["confidence"] == 0
    
    def test_multilingual_classification(self):
        """Тест многоязычной классификации"""
        text = """
        Invoice number 123
        Client information
        Total amount with VAT
        """
        
        result = classify_document(text)
        
        assert result["type"] == "Factură/Счет"
        assert result["confidence"] > 0
    
    def test_classification_confidence_calculation(self):
        """Тест расчета уверенности классификации"""
        # Текст с несколькими ключевыми словами для налогового документа
        text = "serviciul fiscal impozit tva declarație"
        
        result = classify_document(text)
        
        # Проверяем, что все типы документов присутствуют в результате
        assert "all_types" in result
        assert len(result["all_types"]) > 0
        
        # Проверяем, что уверенность рассчитана для всех типов
        for doc_type, config in result["all_types"].items():
            assert "confidence" in config
            assert isinstance(config["confidence"], (int, float))


class TestConfiguration:
    """Тесты для конфигурации"""
    
    def test_config_validation(self):
        """Тест валидации конфигурации"""
        # Конфигурация должна быть валидной
        assert config.validate_config() is True
    
    def test_tesseract_path_detection(self):
        """Тест определения пути к Tesseract"""
        path = config.get_tesseract_path()
        assert isinstance(path, str)
        assert len(path) > 0
    
    def test_document_types_config(self):
        """Тест конфигурации типов документов"""
        assert len(config.DOCUMENT_TYPES) > 0
        
        for doc_type, config_data in config.DOCUMENT_TYPES.items():
            assert "keywords" in config_data
            assert isinstance(config_data["keywords"], list)
            assert len(config_data["keywords"]) > 0
    
    def test_allowed_extensions(self):
        """Тест разрешенных расширений файлов"""
        assert len(config.ALLOWED_EXTENSIONS) > 0
        assert '.pdf' in config.ALLOWED_EXTENSIONS
        assert '.png' in config.ALLOWED_EXTENSIONS


class TestIntegration:
    """Интеграционные тесты"""
    
    @patch('main.pytesseract.image_to_string')
    def test_full_processing_pipeline(self, mock_ocr):
        """Тест полного пайплайна обработки"""
        mock_ocr.return_value = "Serviciul Fiscal de Stat declarație impozit"
        
        # Создаем временное изображение
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            img = Image.new('RGB', (100, 100), color='white')
            img.save(tmp_file.name)
            
            try:
                # Извлекаем текст
                text = extract_text_from_image(tmp_file.name)
                assert "Serviciul Fiscal de Stat" in text
                
                # Классифицируем документ
                result = classify_document(text)
                assert result["type"] == "Serviciul Fiscal de Stat (Налоговая служба)"
                assert result["confidence"] > 0
                
            finally:
                os.unlink(tmp_file.name)


if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v"]) 