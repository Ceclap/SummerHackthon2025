"""
Инструменты для конвертации файлов между различными форматами
"""

import io
import logging
from typing import Union, List
from pathlib import Path
import pandas as pd
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
import csv

logger = logging.getLogger(__name__)

class ConversionTools:
    """Инструменты для конвертации файлов"""
    
    @staticmethod
    def convert_image_to_pdf(image_bytes: bytes, output_path: str) -> None:
        """Конвертация изображения в PDF"""
        try:
            # Открытие изображения
            image = Image.open(io.BytesIO(image_bytes))
            
            # Создание PDF
            c = canvas.Canvas(output_path, pagesize=A4)
            width, height = A4
            
            # Масштабирование изображения под размер страницы
            img_width, img_height = image.size
            aspect = img_width / img_height
            page_aspect = width / height
            
            if aspect > page_aspect:
                # Изображение шире страницы
                new_width = width - 40  # Отступы 20px с каждой стороны
                new_height = new_width / aspect
            else:
                # Изображение выше страницы
                new_height = height - 40
                new_width = new_height * aspect
            
            # Центрирование изображения
            x = (width - new_width) / 2
            y = (height - new_height) / 2
            
            # Сохранение изображения во временный буфер
            img_buffer = io.BytesIO()
            image.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            # Добавление изображения в PDF
            c.drawImage(ImageReader(img_buffer), x, y, new_width, new_height)
            c.save()
            
            logger.info(f"Изображение успешно конвертировано в PDF: {output_path}")
            
        except Exception as e:
            logger.error(f"Ошибка конвертации изображения в PDF: {e}")
            raise
    
    @staticmethod
    def convert_photo_to_excel(image_bytes: bytes) -> bytes:
        """Конвертация фотографии таблицы в Excel"""
        try:
            # Здесь должна быть логика OCR для извлечения таблицы
            # Пока создаем простую таблицу-заглушку
            
            # Создание DataFrame с примерными данными
            data = {
                'Колонка 1': ['Данные 1', 'Данные 2', 'Данные 3'],
                'Колонка 2': [100, 200, 300],
                'Колонка 3': ['A', 'B', 'C']
            }
            df = pd.DataFrame(data)
            
            # Сохранение в Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Таблица')
            
            output.seek(0)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Ошибка конвертации в Excel: {e}")
            raise
    
    @staticmethod
    def convert_photo_to_csv(image_bytes: bytes) -> bytes:
        """Конвертация фотографии таблицы в CSV"""
        try:
            # Здесь должна быть логика OCR для извлечения таблицы
            # Пока создаем простую таблицу-заглушку
            
            # Создание данных
            data = [
                ['Колонка 1', 'Колонка 2', 'Колонка 3'],
                ['Данные 1', '100', 'A'],
                ['Данные 2', '200', 'B'],
                ['Данные 3', '300', 'C']
            ]
            
            # Сохранение в CSV
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerows(data)
            
            return output.getvalue().encode('utf-8')
            
        except Exception as e:
            logger.error(f"Ошибка конвертации в CSV: {e}")
            raise
    
    @staticmethod
    def extract_table_from_image(image_bytes: bytes) -> List[List[str]]:
        """Извлечение таблицы из изображения с помощью OCR"""
        try:
            # Здесь должна быть реализация OCR для извлечения таблицы
            # Пока возвращаем заглушку
            
            # В реальной реализации здесь будет:
            # 1. OCR распознавание текста
            # 2. Определение структуры таблицы
            # 3. Извлечение данных по ячейкам
            
            return [
                ['Колонка 1', 'Колонка 2', 'Колонка 3'],
                ['Данные 1', '100', 'A'],
                ['Данные 2', '200', 'B'],
                ['Данные 3', '300', 'C']
            ]
            
        except Exception as e:
            logger.error(f"Ошибка извлечения таблицы: {e}")
            raise

# Создание глобального экземпляра
conversion_tools = ConversionTools() 