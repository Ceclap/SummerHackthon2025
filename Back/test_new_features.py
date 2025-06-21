#!/usr/bin/env python3
"""
Тестовый скрипт для демонстрации новых возможностей AI Помощника Бухгалтера
"""

import requests
import json
from datetime import datetime

# Базовый URL API
BASE_URL = "http://localhost:8000"

def test_health():
    """Тест проверки состояния сервиса"""
    print("🔍 Проверка состояния сервиса...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Сервис работает: {data['app_name']} v{data['version']}")
        print(f"   OpenAI доступен: {data['openai_available']}")
        print(f"   Tesseract доступен: {data['tesseract_available']}")
        return True
    else:
        print(f"❌ Ошибка: {response.status_code}")
        return False

def test_document_classifier():
    """Тест классификатора документов"""
    print("\n🧾 Тест классификатора документов...")
    
    # Тестовые тексты для разных типов документов
    test_documents = {
        "factura_fiscala": """
        FACTURĂ FISCALĂ
        Nr. F-001/2024
        Data: 01.01.2024
        Furnizor: SRL "Test Company"
        IDNO: 1234567890123
        Client: SRL "Client Company"
        IDNO: 9876543210987
        Suma fără TVA: 1000.00 MDL
        TVA (20%): 200.00 MDL
        Total: 1200.00 MDL
        """,
        
        "bon_fiscal": """
        BON FISCAL
        Terminal Fiscal: TF-123456
        Data: 01.01.2024
        Ora: 14:30:25
        
        Produs 1         2 x 50.00 = 100.00
        Produs 2         1 x 25.00 = 25.00
        
        Total: 125.00 MDL
        """,
        
        "stat_plata": """
        STAT DE PLATĂ
        Luna: Ianuarie 2024
        
        Nume Prenume    Poziția    Salariu    Taxe    Contribuții
        Ivanov Ivan    Contabil   5000.00   500.00   250.00
        Petrov Petru   Manager    8000.00   800.00   400.00
        
        Total: 13000.00 MDL
        """
    }
    
    for doc_type, text in test_documents.items():
        print(f"\n📄 Тестируем: {doc_type}")
        
        # Создаем временный файл для тестирования
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(text)
            temp_file_path = f.name
        
        try:
            # Отправляем файл на обработку
            with open(temp_file_path, 'rb') as f:
                files = {'file': ('test_doc.txt', f, 'text/plain')}
                response = requests.post(f"{BASE_URL}/documents/upload", files=files)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Документ обработан:")
                print(f"   Тип: {data['doc_type']}")
                print(f"   Уверенность: {data['confidence']:.1f}%")
                print(f"   Извлеченные поля: {len(data['fields'])}")
                
                if data['validation_errors']:
                    print(f"   ⚠️ Ошибки: {data['validation_errors']}")
                if data['validation_warnings']:
                    print(f"   ⚠️ Предупреждения: {data['validation_warnings']}")
            else:
                print(f"❌ Ошибка обработки: {response.status_code}")
                print(f"   Ответ: {response.text}")
                
        finally:
            # Удаляем временный файл
            os.unlink(temp_file_path)

def test_document_search():
    """Тест поиска документов"""
    print("\n🔍 Тест поиска документов...")
    
    # Поиск всех документов
    response = requests.get(f"{BASE_URL}/documents")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Найдено документов: {data['total_count']}")
        
        if data['documents']:
            print("📋 Список документов:")
            for doc in data['documents']:
                print(f"   ID: {doc['id']}, Тип: {doc['doc_type']}, Файл: {doc['filename']}")
        else:
            print("   📭 Документы не найдены")
    else:
        print(f"❌ Ошибка поиска: {response.status_code}")

def test_reports():
    """Тест генерации отчетов"""
    print("\n📊 Тест генерации отчетов...")
    
    # Сводный отчет
    print("📈 Сводный отчет:")
    response = requests.get(f"{BASE_URL}/reports/summary")
    if response.status_code == 200:
        data = response.json()
        print(f"   Всего документов: {data['summary']['total_documents']}")
        print(f"   По типам: {data['summary']['by_type']}")
    else:
        print(f"   ❌ Ошибка: {response.status_code}")
    
    # Детальный отчет
    print("\n📋 Детальный отчет:")
    response = requests.get(f"{BASE_URL}/reports/detailed")
    if response.status_code == 200:
        data = response.json()
        print(f"   Документов в отчете: {data['total_count']}")
    else:
        print(f"   ❌ Ошибка: {response.status_code}")

def test_fiscal_report():
    """Тест отчета для FISC"""
    print("\n🏛️ Тест отчета для FISC...")
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    response = requests.get(f"{BASE_URL}/reports/fiscal?month={current_month}&year={current_year}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Отчет FISC сгенерирован:")
        print(f"   Период: {data['period']}")
        print(f"   Всего фактур: {data['total_invoices']}")
        print(f"   Общая сумма: {data['total_amount']:.2f} MDL")
        print(f"   Общий НДС: {data['total_vat']:.2f} MDL")
    else:
        print(f"❌ Ошибка генерации отчета FISC: {response.status_code}")

def test_export_reports():
    """Тест экспорта отчетов"""
    print("\n📤 Тест экспорта отчетов...")
    
    # Экспорт сводного отчета в JSON
    print("📄 Экспорт сводного отчета в JSON:")
    response = requests.get(f"{BASE_URL}/reports/export?report_type=summary&format=json")
    if response.status_code == 200:
        print("✅ Отчет успешно экспортирован в JSON")
        # Сохраняем файл
        filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"   Файл сохранен: {filename}")
    else:
        print(f"❌ Ошибка экспорта: {response.status_code}")

def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование новых возможностей AI Помощника Бухгалтера")
    print("=" * 60)
    
    # Проверяем состояние сервиса
    if not test_health():
        print("❌ Сервис недоступен. Убедитесь, что приложение запущено.")
        return
    
    # Тестируем классификатор документов
    test_document_classifier()
    
    # Тестируем поиск документов
    test_document_search()
    
    # Тестируем генерацию отчетов
    test_reports()
    
    # Тестируем отчет для FISC
    test_fiscal_report()
    
    # Тестируем экспорт отчетов
    test_export_reports()
    
    print("\n" + "=" * 60)
    print("✅ Тестирование завершено!")
    print("\n📚 Дополнительная информация:")
    print("   - API документация: http://localhost:8000/docs")
    print("   - Веб-интерфейс: http://localhost:8000/")
    print("   - Проверка состояния: http://localhost:8000/health")

if __name__ == "__main__":
    main() 