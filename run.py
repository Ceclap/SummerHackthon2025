#!/usr/bin/env python3
"""
Скрипт для запуска AI Помощника Бухгалтера в продакшн режиме
"""

import uvicorn
import argparse
import sys
import os
from config import config

def main():
    """Основная функция запуска"""
    parser = argparse.ArgumentParser(description='AI Помощник Бухгалтера')
    parser.add_argument(
        '--host', 
        default=config.HOST, 
        help=f'Хост для запуска (по умолчанию: {config.HOST})'
    )
    parser.add_argument(
        '--port', 
        type=int, 
        default=config.PORT, 
        help=f'Порт для запуска (по умолчанию: {config.PORT})'
    )
    parser.add_argument(
        '--workers', 
        type=int, 
        default=1, 
        help='Количество воркеров (по умолчанию: 1)'
    )
    parser.add_argument(
        '--reload', 
        action='store_true', 
        help='Автоперезагрузка при изменении файлов (только для разработки)'
    )
    parser.add_argument(
        '--log-level', 
        default=config.LOG_LEVEL.lower(), 
        choices=['debug', 'info', 'warning', 'error'],
        help=f'Уровень логирования (по умолчанию: {config.LOG_LEVEL.lower()})'
    )
    
    args = parser.parse_args()
    
    # Проверяем, что Tesseract установлен
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        print(f"✓ Tesseract найден: {pytesseract.get_tesseract_version()}")
    except Exception as e:
        print(f"✗ Ошибка: Tesseract не найден или не настроен: {e}")
        print("Установите Tesseract OCR и языковые пакеты:")
        print("  macOS: brew install tesseract tesseract-lang")
        print("  Ubuntu: sudo apt install tesseract-ocr tesseract-ocr-ron tesseract-ocr-rus tesseract-ocr-eng")
        print("  Windows: Скачайте с https://github.com/UB-Mannheim/tesseract/wiki")
        sys.exit(1)
    
    # Проверяем конфигурацию
    try:
        config.validate_config()
        print("✓ Конфигурация валидна")
    except Exception as e:
        print(f"✗ Ошибка конфигурации: {e}")
        sys.exit(1)
    
    # Создаем необходимые директории
    config.create_directories()
    print("✓ Директории созданы")
    
    print(f"🚀 Запуск {config.APP_NAME} версии {config.APP_VERSION}")
    print(f"📍 Адрес: http://{args.host}:{args.port}")
    print(f"📚 API документация: http://{args.host}:{args.port}/docs")
    print(f"🔍 Проверка состояния: http://{args.host}:{args.port}/health")
    
    if args.reload:
        print("🔄 Режим автоперезагрузки включен (только для разработки)")
    
    # Запускаем сервер
    uvicorn.run(
        "main:app",
        host=args.host,
        port=args.port,
        workers=args.workers if not args.reload else 1,
        reload=args.reload,
        log_level=args.log_level,
        access_log=True
    )

if __name__ == "__main__":
    main() 