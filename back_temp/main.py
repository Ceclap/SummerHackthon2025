"""
Главный модуль AI Помощник Бухгалтера Молдовы
Включает API endpoints и веб-интерфейс
"""

import os
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import pandas as pd
from fastapi.templating import Jinja2Templates
import io

from config import config
from i18n import i18n
from document_processor import document_processor
from document_storage import DocumentStorage
from data_models import (
    DocumentData, DocumentResponse, UploadResponse, ReportRequest, LanguageRequest
)
from report_generator_v2 import report_generator_v2
from conversion_tools import conversion_tools

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создание FastAPI приложения
app = FastAPI(
    title="AI Помощник Бухгалтера Молдова",
    version=config.VERSION,
    description="Умная система для обработки и анализа бухгалтерских документов в Молдове.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Определение путей к шаблонам и статическим файлам
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

templates = Jinja2Templates(directory=TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация компонентов
storage = DocumentStorage()
# report_gen = ReportGenerator(storage) # Удалено, используется report_generator_v2

# Модели данных
# Перенесены в data_models.py

# Функции зависимостей
def get_language(lang: str = Query("ru", description="Язык интерфейса")):
    """Получение языка из query параметра"""
    if lang not in ["ru", "ro"]:
        lang = "ru"
    return lang

# API Endpoints

@app.get("/", response_class=HTMLResponse)
async def root(request: Request, language: str = Depends(get_language)):
    """Главная страница с 4 разделами"""
    i18n.set_language(language)
    return templates.TemplateResponse("index.html", {"request": request, "language": language, "config": config})

@app.get("/health")
async def health_check():
    """Проверка состояния сервера"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": config.VERSION,
        "app_name": config.APP_NAME,
        "openai_available": bool(config.OPENAI_API_KEY),
        "tesseract_available": bool(config.TESSERACT_PATH)
    }

@app.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    language: str = Query("ru", description="Язык документа")
):
    """Загрузка и обработка документа"""
    try:
        logger.info(f"Получен файл: {file.filename}")
        
        # Проверка размера файла
        if file.size > config.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=i18n.get_text("error_file_too_large"))
        
        # Проверка расширения файла
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in config.ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=i18n.get_text("error_invalid_format"))
        
        # Сохранение файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{file.filename}"
        file_path = config.UPLOADS_DIR / unique_filename
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Файл сохранен: {file_path}, размер: {len(content)} байт")
        
        # Обработка документа
        doc_data, validation_result = document_processor.process_document(str(file_path), language)
        
        if not doc_data:
            os.remove(file_path) # Удаляем файл, если обработка не удалась
            error_message = (validation_result.get("errors") or ["Unknown processing error"])[0]
            raise HTTPException(status_code=400, detail=error_message)

        # Сохранение документа в базу данных
        doc_id = storage.store_document(
            doc_data,
            file.filename, # Сохраняем оригинальное имя файла
            str(file_path),
            validation_result
        )
        
        # Файл не удаляется сразу, а сохраняется для скачивания
        # os.remove(file_path) 
        
        extracted_data_dict = {field.name: field.value for field in doc_data.fields}

        return UploadResponse(
            success=True,
            message=i18n.get_text("message_processing_complete", language),
            document_type=doc_data.doc_type,
            confidence=doc_data.confidence,
            extracted_data=extracted_data_dict,
            language=language
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка загрузки документа: {e}", exc_info=True)
        # Удаляем файл в случае любой ошибки после его создания
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {e}")

@app.get("/documents", response_model=List[DocumentResponse])
async def get_documents(
    start_date: Optional[str] = Query(None, description="Начальная дата (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Конечная дата (YYYY-MM-DD)"),
    doc_type: Optional[str] = Query(None, description="Тип документа"),
    status: Optional[str] = Query(None, description="Статус документа (pending, processed, archived)"),
    search: Optional[str] = Query(None, description="Поиск по тексту"),
    date_from: Optional[str] = Query(None, description="Дата от (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Дата до (YYYY-MM-DD)"),
    language: str = Depends(get_language)
):
    """Получение списка документов с фильтрацией"""
    try:
        i18n.set_language(language)
        
        # Построение фильтров
        filters = {}
        if start_date:
            filters["start_date"] = start_date
        if end_date:
            filters["end_date"] = end_date
        if doc_type:
            filters["doc_type"] = doc_type
        if status:
            filters["status"] = status
        if search:
            filters["search"] = search
        if date_from:
            filters["date_from"] = date_from
        if date_to:
            filters["date_to"] = date_to
        
        documents = storage.get_documents(filters)
        
        # Преобразование в формат ответа
        response_docs = []
        for doc in documents:
            response_docs.append(DocumentResponse(
                id=doc.id,
                filename=doc.filename,
                document_type=doc.document_type,
                processing_date=doc.processing_date.isoformat() if doc.processing_date else "",
                confidence=doc.confidence,
                extracted_data=doc.extracted_data,
                is_valid=doc.is_valid,
                validation_errors=doc.validation_errors or [],
                status="pending" if doc.validation_errors else "processed"
            ))
        
        return response_docs
        
    except Exception as e:
        logger.error(f"Ошибка получения документов: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents/pending", response_model=List[DocumentResponse])
async def get_pending_documents(language: str = Depends(get_language)):
    """Получение документов для проверки и исправления"""
    try:
        i18n.set_language(language)
        
        # Получаем документы со статусом "pending" или с ошибками валидации
        filters = {"status": "pending"}
        documents = storage.get_documents(filters)
        
        # Также добавляем документы с ошибками валидации
        error_filters = {"has_validation_errors": True}
        error_documents = storage.get_documents(error_filters)
        
        # Объединяем и убираем дубликаты
        all_docs = documents + error_documents
        unique_docs = {doc.id: doc for doc in all_docs}.values()
        
        response_docs = []
        for doc in unique_docs:
            response_docs.append(DocumentResponse(
                id=doc.id,
                filename=doc.filename,
                document_type=doc.document_type,
                processing_date=doc.processing_date.isoformat() if doc.processing_date else "",
                confidence=doc.confidence,
                extracted_data=doc.extracted_data,
                is_valid=doc.is_valid,
                validation_errors=doc.validation_errors or [],
                status="pending" if doc.validation_errors else "processed"
            ))
        
        return response_docs
        
    except Exception as e:
        logger.error(f"Ошибка получения документов для проверки: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/documents/{doc_id}/edit")
async def edit_document(
    doc_id: int,
    request: Request,
    language: str = Depends(get_language)
):
    """Редактирование документа"""
    try:
        i18n.set_language(language)
        
        # Получаем данные для редактирования
        data = await request.json()
        updated_fields = data.get("fields", {})
        
        # Обновляем документ в базе данных
        success = storage.update_document(doc_id, updated_fields)
        
        if not success:
            raise HTTPException(status_code=404, detail="Документ не найден")
        
        return {"success": True, "message": "Документ успешно обновлен"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка редактирования документа: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents/{doc_id}/download")
async def download_document(doc_id: int):
    """Скачивание документа"""
    try:
        # Получаем информацию о документе
        doc = storage.get_document(doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Документ не найден")
        
        # Путь к файлу
        file_path = Path(doc.file_path)
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Файл не найден")
        
        return FileResponse(
            path=str(file_path),
            filename=doc.filename,
            media_type='application/octet-stream'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка скачивания документа: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents/{doc_id}/preview")
async def preview_document(doc_id: int, language: str = Depends(get_language)):
    """Предварительный просмотр документа"""
    try:
        i18n.set_language(language)
        
        # Получаем документ в формате для API
        doc_api_format = storage.get_document_for_api(doc_id)
        
        if not doc_api_format:
            raise HTTPException(status_code=404, detail="Документ не найден")
            
        return doc_api_format
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка предварительного просмотра: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reports/generate")
async def generate_report(request: ReportRequest):
    """Генерация отчёта"""
    try:
        i18n.set_language(request.language)
        
        if request.report_type == "summary":
            report = report_generator_v2.generate_summary_report(
                request.start_date, request.end_date, request.language
            )
        elif request.report_type == "fiscal":
            # Извлечение месяца и года из даты
            if request.start_date:
                start_date = datetime.fromisoformat(request.start_date)
                month, year = start_date.month, start_date.year
            else:
                now = datetime.now()
                month, year = now.month, now.year
            
            report = report_generator_v2.generate_fiscal_report(month, year, request.language)
        elif request.report_type == "detailed":
            report = report_generator_v2.generate_detailed_report(
                request.start_date, request.end_date, None, request.language
            )
        else:
            raise HTTPException(status_code=400, detail="Неизвестный тип отчёта")
        
        if "error" in report:
            raise HTTPException(status_code=500, detail=report["error"])
        
        # Экспорт отчёта
        filename = f"report_{request.report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{request.format}"
        file_path = report_generator_v2.export_report(report, request.format, filename)
        
        return {
            "success": True,
            "message": i18n.get_text("report_generated", request.language),
            "download_url": f"/reports/download/{filename}",
            "report": report
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка генерации отчёта: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reports/download/{filename}")
async def download_report(filename: str):
    """Скачивание сгенерированного отчета"""
    report_path = config.REPORTS_DIR / filename
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Отчет не найден")
    return FileResponse(str(report_path), media_type='application/octet-stream', filename=filename)

@app.get("/statistics")
async def get_statistics(language: str = Depends(get_language)):
    """Получение статистики по документам для графиков"""
    try:
        stats = storage.get_statistics()
        return stats
    except Exception as e:
        logger.error(f"Ошибка при получении статистики: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Не удалось загрузить статистику")

@app.post("/language")
async def set_language(request: LanguageRequest):
    """Установка языка интерфейса (через cookie или сессию)"""
    try:
        if request.language not in ["ru", "ro"]:
            raise HTTPException(status_code=400, detail="Неподдерживаемый язык")
        
        i18n.set_language(request.language)
        return {"success": True, "language": request.language}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка установки языка: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/languages")
async def get_supported_languages():
    """Получение списка поддерживаемых языков"""
    return i18n.get_supported_languages()

@app.post("/tools/photo-to-excel")
async def photo_to_excel(file: UploadFile = File(...)):
    """Конвертация фото с таблицей в Excel. (демо-версия)"""
    try:
        image_bytes = await file.read()
        excel_bytes = conversion_tools.convert_photo_to_excel(image_bytes)
        
        return FileResponse(
            io.BytesIO(excel_bytes),
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            filename="converted_table.xlsx"
        )
    except Exception as e:
        logger.error(f"Ошибка конвертации фото в Excel: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/convert-to-pdf")
async def convert_to_pdf(file: UploadFile = File(...)):
    """Конвертация файла в PDF"""
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Поддерживаются только изображения")
        
        # Создание временного файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{Path(file.filename).stem}.pdf"
        file_path = config.UPLOADS_DIR / filename
        
        # Конвертация изображения в PDF
        image_bytes = await file.read()
        
        # Используем глобальный экземпляр
        conversion_tools.convert_image_to_pdf(image_bytes, str(file_path))
        
        return {"success": True, "filename": filename}
        
    except Exception as e:
        logger.error(f"Ошибка конвертации в PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/convert-to-excel")
async def convert_to_excel(file: UploadFile = File(...)):
    """Конвертация файла в Excel"""
    try:
        image_bytes = await file.read()
        
        # Используем глобальный экземпляр
        excel_bytes = conversion_tools.convert_photo_to_excel(image_bytes)
        
        # Сохранение файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{Path(file.filename).stem}.xlsx"
        file_path = config.UPLOADS_DIR / filename
        
        with open(file_path, "wb") as f:
            f.write(excel_bytes)
        
        return {"success": True, "filename": filename}
        
    except Exception as e:
        logger.error(f"Ошибка конвертации в Excel: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/convert-to-csv")
async def convert_to_csv(file: UploadFile = File(...)):
    """Конвертация файла в CSV"""
    try:
        image_bytes = await file.read()
        
        # Используем глобальный экземпляр
        csv_bytes = conversion_tools.convert_photo_to_csv(image_bytes)
        
        # Сохранение файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{Path(file.filename).stem}.csv"
        file_path = config.UPLOADS_DIR / filename
        
        with open(file_path, "wb") as f:
            f.write(csv_bytes)
        
        return {"success": True, "filename": filename}
        
    except Exception as e:
        logger.error(f"Ошибка конвертации в CSV: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Скачивание файла"""
    try:
        file_path = config.UPLOADS_DIR / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Файл не найден")
        
        return FileResponse(file_path, filename=filename)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка скачивания файла: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Новые эндпоинты для финансовой автоматизации

@app.get("/workflows")
async def get_workflows(language: str = Depends(get_language)):
    """Получение списка рабочих процессов"""
    try:
        i18n.set_language(language)
        
        # Пример рабочих процессов
        workflows = [
            {
                "id": 1,
                "name": "Обработка счетов-фактур",
                "description": "Автоматическая обработка и валидация счетов-фактур",
                "status": "active",
                "steps": ["Загрузка", "OCR", "Валидация", "Утверждение"],
                "created_at": "2025-01-15T10:00:00Z"
            },
            {
                "id": 2,
                "name": "Согласование расходов",
                "description": "Процесс согласования и утверждения расходов",
                "status": "active",
                "steps": ["Создание", "Проверка", "Согласование", "Оплата"],
                "created_at": "2025-01-10T14:30:00Z"
            },
            {
                "id": 3,
                "name": "Интеграция с ERP",
                "description": "Автоматическая синхронизация данных с ERP системой",
                "status": "active",
                "steps": ["Извлечение", "Трансформация", "Загрузка", "Проверка"],
                "created_at": "2025-01-05T09:15:00Z"
            }
        ]
        
        return {"workflows": workflows}
        
    except Exception as e:
        logger.error(f"Ошибка получения рабочих процессов: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workflows")
async def create_workflow(request: Request, language: str = Depends(get_language)):
    """Создание нового рабочего процесса"""
    try:
        i18n.set_language(language)
        
        data = await request.json()
        workflow_name = data.get("name")
        workflow_description = data.get("description")
        workflow_steps = data.get("steps", [])
        
        if not workflow_name:
            raise HTTPException(status_code=400, detail="Название рабочего процесса обязательно")
        
        # Здесь должна быть логика сохранения в базу данных
        new_workflow = {
            "id": 4,  # Генерируется автоматически
            "name": workflow_name,
            "description": workflow_description,
            "status": "active",
            "steps": workflow_steps,
            "created_at": datetime.now().isoformat()
        }
        
        return {"success": True, "workflow": new_workflow}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка создания рабочего процесса: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/integrations")
async def get_integrations(language: str = Depends(get_language)):
    """Получение списка интеграций"""
    try:
        i18n.set_language(language)
        
        integrations = [
            {
                "id": 1,
                "name": "SAP ERP",
                "type": "erp",
                "status": "connected",
                "last_sync": "2025-01-21T15:30:00Z",
                "sync_frequency": "hourly"
            },
            {
                "id": 2,
                "name": "Oracle NetSuite",
                "type": "erp",
                "status": "available",
                "last_sync": None,
                "sync_frequency": "daily"
            },
            {
                "id": 3,
                "name": "Microsoft Dynamics",
                "type": "erp",
                "status": "available",
                "last_sync": None,
                "sync_frequency": "daily"
            },
            {
                "id": 4,
                "name": "Gmail",
                "type": "email",
                "status": "connected",
                "last_sync": "2025-01-21T16:00:00Z",
                "sync_frequency": "realtime"
            },
            {
                "id": 5,
                "name": "Outlook",
                "type": "email",
                "status": "available",
                "last_sync": None,
                "sync_frequency": "realtime"
            }
        ]
        
        return {"integrations": integrations}
        
    except Exception as e:
        logger.error(f"Ошибка получения интеграций: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/integrations/{integration_id}/connect")
async def connect_integration(integration_id: int, request: Request):
    """Подключение интеграции"""
    try:
        data = await request.json()
        credentials = data.get("credentials", {})
        
        # Здесь должна быть логика подключения интеграции
        # Например, проверка учетных данных и установка соединения
        
        return {
            "success": True,
            "message": f"Интеграция {integration_id} успешно подключена",
            "status": "connected",
            "last_sync": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Ошибка подключения интеграции: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
async def get_analytics(
    period: str = Query("month", description="Период: day, week, month, year"),
    language: str = Depends(get_language)
):
    """Получение аналитики"""
    try:
        i18n.set_language(language)
        
        # Пример аналитических данных
        analytics = {
            "period": period,
            "documents_processed": {
                "total": 1250,
                "this_period": 89,
                "growth": 12.5
            },
            "processing_time": {
                "average": 2.3,
                "min": 0.5,
                "max": 8.1
            },
            "accuracy": {
                "overall": 98.5,
                "by_type": {
                    "invoice": 99.2,
                    "receipt": 97.8,
                    "contract": 98.9
                }
            },
            "cost_savings": {
                "total": 45000,
                "this_period": 3200,
                "currency": "USD"
            },
            "top_document_types": [
                {"type": "invoice", "count": 456, "percentage": 36.5},
                {"type": "receipt", "count": 234, "percentage": 18.7},
                {"type": "contract", "count": 189, "percentage": 15.1}
            ]
        }
        
        return analytics
        
    except Exception as e:
        logger.error(f"Ошибка получения аналитики: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/automation-rules")
async def get_automation_rules(language: str = Depends(get_language)):
    """Получение правил автоматизации"""
    try:
        i18n.set_language(language)
        
        rules = [
            {
                "id": 1,
                "name": "Автоматическое утверждение счетов до 1000",
                "description": "Счета-фактуры на сумму до 1000 автоматически утверждаются",
                "conditions": [
                    {"field": "amount", "operator": "<=", "value": 1000},
                    {"field": "document_type", "operator": "==", "value": "invoice"}
                ],
                "actions": [
                    {"type": "approve", "parameters": {}},
                    {"type": "notify", "parameters": {"recipient": "manager"}}
                ],
                "status": "active"
            },
            {
                "id": 2,
                "name": "Проверка дубликатов",
                "description": "Автоматическая проверка на дублирование документов",
                "conditions": [
                    {"field": "vendor_id", "operator": "exists", "value": True},
                    {"field": "amount", "operator": "exists", "value": True}
                ],
                "actions": [
                    {"type": "flag_duplicate", "parameters": {}},
                    {"type": "notify", "parameters": {"recipient": "admin"}}
                ],
                "status": "active"
            }
        ]
        
        return {"rules": rules}
        
    except Exception as e:
        logger.error(f"Ошибка получения правил автоматизации: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/automation-rules")
async def create_automation_rule(request: Request, language: str = Depends(get_language)):
    """Создание нового правила автоматизации"""
    try:
        i18n.set_language(language)
        
        data = await request.json()
        rule_name = data.get("name")
        rule_description = data.get("description")
        conditions = data.get("conditions", [])
        actions = data.get("actions", [])
        
        if not rule_name:
            raise HTTPException(status_code=400, detail="Название правила обязательно")
        
        # Здесь должна быть логика сохранения в базу данных
        new_rule = {
            "id": 3,  # Генерируется автоматически
            "name": rule_name,
            "description": rule_description,
            "conditions": conditions,
            "actions": actions,
            "status": "active",
            "created_at": datetime.now().isoformat()
        }
        
        return {"success": True, "rule": new_rule}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка создания правила автоматизации: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api-status")
async def get_api_status():
    """Статус API и внешних сервисов"""
    try:
        status = {
            "api": "healthy",
            "database": "healthy",
            "openai": "healthy" if config.OPENAI_API_KEY else "unavailable",
            "tesseract": "healthy" if config.TESSERACT_PATH else "unavailable",
            "storage": "healthy",
            "timestamp": datetime.now().isoformat()
        }
        
        return status
        
    except Exception as e:
        logger.error(f"Ошибка получения статуса API: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Запуск приложения
if __name__ == "__main__":
    # Валидация конфигурации
    config.validate_config()
    
    print(f"🚀 Запуск {config.APP_NAME} версии {config.APP_VERSION}")
    print(f"📍 Адрес: http://{config.HOST}:{config.PORT}")
    print(f"📚 API документация: http://{config.HOST}:{config.PORT}/docs")
    print(f"🔍 Проверка состояния: http://{config.HOST}:{config.PORT}/health")
    
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level="info"
    )

