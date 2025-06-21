from dataclasses import dataclass, field
from typing import List, Any, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

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

# --- Pydantic модели для API ---

class UploadResponse(BaseModel):
    """Ответ на успешную загрузку документа"""
    success: bool
    message: str
    document_type: Optional[str] = None
    confidence: Optional[float] = None
    extracted_data: Optional[Dict[str, Any]] = None
    language: str = "ru"

class DocumentResponse(BaseModel):
    """Модель документа для API ответов"""
    id: int
    filename: str
    document_type: str
    processing_date: str
    confidence: float
    extracted_data: Dict[str, Any]
    is_valid: bool
    validation_errors: List[str]
    status: str

class ReportRequest(BaseModel):
    """Запрос на генерацию отчета"""
    report_type: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    language: str = "ru"
    format: str = "json"
    parameters: Optional[Dict[str, Any]] = None

class LanguageRequest(BaseModel):
    """Запрос на смену языка"""
    language: str 