import json
import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, date
from dataclasses import dataclass, asdict
from pathlib import Path
import sqlite3
from data_models import DocumentData, DocumentField

logger = logging.getLogger(__name__)

@dataclass
class StoredDocument:
    """Сохраненный документ в базе данных"""
    id: int
    filename: str
    doc_type: str
    fields: List[DocumentField]
    raw_text: str
    upload_date: datetime
    file_path: str
    confidence: float = 1.0
    validation_errors: List[str] = None
    validation_warnings: List[str] = None
    
    @property
    def document_type(self) -> str:
        """Совместимость с API"""
        return self.doc_type
    
    @property
    def processing_date(self) -> datetime:
        """Совместимость с API"""
        return self.upload_date
    
    @property
    def extracted_data(self) -> Dict[str, str]:
        """Извлеченные данные в формате словаря"""
        return {field.name: field.value for field in self.fields}
    
    @property
    def is_valid(self) -> bool:
        """Проверка валидности документа"""
        return len(self.validation_errors or []) == 0

class DocumentStorage:
    """Хранилище документов с базой данных SQLite"""
    
    def __init__(self, db_path: str = "documents.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Создание таблицы документов
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS documents (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filename TEXT NOT NULL,
                        doc_type TEXT NOT NULL,
                        fields TEXT NOT NULL,
                        raw_text TEXT,
                        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        file_path TEXT NOT NULL,
                        confidence REAL DEFAULT 1.0,
                        validation_errors TEXT,
                        validation_warnings TEXT
                    )
                """)
                
                # Создание индексов для быстрого поиска
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_doc_type ON documents(doc_type)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_upload_date ON documents(upload_date)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_filename ON documents(filename)")
                
                conn.commit()
                logger.info("База данных документов инициализирована")
                
        except Exception as e:
            logger.error(f"Ошибка инициализации базы данных: {e}")
            raise
    
    def store_document(self, doc_data: DocumentData, filename: str, file_path: str, 
                      validation_result: Dict[str, List[str]] = None) -> int:
        """Сохраняет документ в базу данных"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Сериализация полей
                fields_json = json.dumps([asdict(field) for field in doc_data.fields])
                
                # Сериализация ошибок валидации
                validation_errors = json.dumps(validation_result.get("errors", [])) if validation_result else None
                validation_warnings = json.dumps(validation_result.get("warnings", [])) if validation_result else None
                
                cursor.execute("""
                    INSERT INTO documents 
                    (filename, doc_type, fields, raw_text, file_path, confidence, validation_errors, validation_warnings)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    filename,
                    doc_data.doc_type,
                    fields_json,
                    doc_data.raw_text,
                    file_path,
                    doc_data.confidence,
                    validation_errors,
                    validation_warnings
                ))
                
                doc_id = cursor.lastrowid
                conn.commit()
                
                logger.info(f"Документ сохранен с ID: {doc_id}")
                return doc_id
                
        except Exception as e:
            logger.error(f"Ошибка сохранения документа: {e}")
            raise
    
    def get_document(self, doc_id: int) -> Optional[StoredDocument]:
        """Получает документ по ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_document(row)
                return None
                
        except Exception as e:
            logger.error(f"Ошибка получения документа: {e}")
            return None
    
    def search_documents(self, 
                        doc_type: Optional[str] = None,
                        idno: Optional[str] = None,
                        date_from: Optional[str] = None,
                        date_to: Optional[str] = None,
                        amount_min: Optional[float] = None,
                        amount_max: Optional[float] = None,
                        filename: Optional[str] = None) -> List[StoredDocument]:
        """Поиск документов по различным критериям"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM documents WHERE 1=1"
                params = []
                
                if doc_type:
                    query += " AND doc_type = ?"
                    params.append(doc_type)
                
                if filename:
                    query += " AND filename LIKE ?"
                    params.append(f"%{filename}%")
                
                if date_from:
                    # Преобразуем строку в объект date
                    try:
                        date_from_obj = datetime.strptime(date_from, "%Y-%m-%d").date()
                        query += " AND DATE(upload_date) >= ?"
                        params.append(date_from_obj.isoformat())
                    except ValueError:
                        logger.warning(f"Неверный формат даты: {date_from}")
                
                if date_to:
                    # Преобразуем строку в объект date
                    try:
                        date_to_obj = datetime.strptime(date_to, "%Y-%m-%d").date()
                        query += " AND DATE(upload_date) <= ?"
                        params.append(date_to_obj.isoformat())
                    except ValueError:
                        logger.warning(f"Неверный формат даты: {date_to}")
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                documents = [self._row_to_document(row) for row in rows]
                
                # Фильтрация по IDNO и суммам (требует парсинга JSON полей)
                if idno or amount_min or amount_max:
                    filtered_docs = []
                    for doc in documents:
                        include = True
                        
                        if idno:
                            idno_field = next((f for f in doc.fields if f.name == "idno"), None)
                            if not idno_field or idno not in idno_field.value:
                                include = False
                        
                        if include and (amount_min or amount_max):
                            amount_fields = [f for f in doc.fields if "amount" in f.name]
                            if amount_fields:
                                try:
                                    amount = float(amount_fields[0].value.replace(",", ""))
                                    if amount_min and amount < amount_min:
                                        include = False
                                    if amount_max and amount > amount_max:
                                        include = False
                                except ValueError:
                                    include = False
                        
                        if include:
                            filtered_docs.append(doc)
                    
                    documents = filtered_docs
                
                logger.info(f"Найдено документов: {len(documents)}")
                return documents
                
        except Exception as e:
            logger.error(f"Ошибка поиска документов: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Собирает статистику по документам в базе."""
        stats = {
            "total_documents": 0,
            "by_type": {},
            "by_status": {
                "valid": 0,
                "invalid": 0
            }
        }
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Total documents
                cursor.execute("SELECT COUNT(*) FROM documents")
                stats["total_documents"] = cursor.fetchone()[0]

                # Documents by type
                cursor.execute("SELECT doc_type, COUNT(*) FROM documents GROUP BY doc_type")
                stats["by_type"] = dict(cursor.fetchall())

                # Documents by status (valid/invalid based on validation_errors)
                cursor.execute("SELECT validation_errors FROM documents")
                rows = cursor.fetchall()
                for row in rows:
                    errors = json.loads(row[0]) if row[0] else []
                    if errors:
                        stats["by_status"]["invalid"] += 1
                    else:
                        stats["by_status"]["valid"] += 1
                
                return stats
        except Exception as e:
            logger.error(f"Ошибка при сборе статистики: {e}")
            return stats
    
    def delete_document(self, doc_id: int) -> bool:
        """Удаляет документ по ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Получаем информацию о файле
                cursor.execute("SELECT file_path FROM documents WHERE id = ?", (doc_id,))
                row = cursor.fetchone()
                
                if row:
                    file_path = row[0]
                    
                    # Удаляем физический файл
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        logger.info(f"Файл удален: {file_path}")
                    
                    # Удаляем запись из БД
                    cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
                    conn.commit()
                    
                    logger.info(f"Документ с ID {doc_id} удален")
                    return True
                
                return False
                
        except Exception as e:
            logger.error(f"Ошибка удаления документа: {e}")
            return False
    
    def _row_to_document(self, row) -> StoredDocument:
        """Преобразует строку БД в объект StoredDocument"""
        try:
            fields_json = json.loads(row[3])
            fields = [DocumentField(**field_data) for field_data in fields_json]
            
            validation_errors = json.loads(row[8]) if row[8] else []
            validation_warnings = json.loads(row[9]) if row[9] else []
            
            # Парсинг даты с обработкой ошибок
            upload_date = None
            try:
                if row[5]:
                    if isinstance(row[5], str):
                        # Пробуем разные форматы даты
                        for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
                            try:
                                upload_date = datetime.strptime(row[5], fmt)
                                break
                            except ValueError:
                                continue
                        if upload_date is None:
                            upload_date = datetime.now()
                    else:
                        upload_date = row[5]
                else:
                    upload_date = datetime.now()
            except Exception:
                upload_date = datetime.now()
            
            return StoredDocument(
                id=row[0],
                filename=row[1],
                doc_type=row[2],
                fields=fields,
                raw_text=row[4],
                upload_date=upload_date,
                file_path=row[6],
                confidence=row[7],
                validation_errors=validation_errors,
                validation_warnings=validation_warnings
            )
        except Exception as e:
            logger.error(f"Ошибка преобразования строки в документ: {e}")
            raise
    
    def get_documents(self, filters: Dict[str, Any] = None) -> List[StoredDocument]:
        """Получение документов с фильтрацией"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM documents WHERE 1=1"
                params = []
                
                if filters:
                    if filters.get("doc_type"):
                        query += " AND doc_type = ?"
                        params.append(filters["doc_type"])
                    
                    if filters.get("status"):
                        if filters["status"] == "pending":
                            query += " AND (validation_errors IS NOT NULL AND validation_errors != '[]')"
                        elif filters["status"] == "processed":
                            query += " AND (validation_errors IS NULL OR validation_errors = '[]')"
                    
                    if filters.get("has_validation_errors"):
                        query += " AND (validation_errors IS NOT NULL AND validation_errors != '[]')"
                    
                    if filters.get("search"):
                        search_term = f"%{filters['search']}%"
                        query += " AND (filename LIKE ? OR raw_text LIKE ?)"
                        params.extend([search_term, search_term])
                    
                    if filters.get("date_from"):
                        try:
                            date_from_obj = datetime.strptime(filters["date_from"], "%Y-%m-%d").date()
                            query += " AND DATE(upload_date) >= ?"
                            params.append(date_from_obj.isoformat())
                        except ValueError:
                            logger.warning(f"Неверный формат даты: {filters['date_from']}")
                    
                    if filters.get("date_to"):
                        try:
                            date_to_obj = datetime.strptime(filters["date_to"], "%Y-%m-%d").date()
                            query += " AND DATE(upload_date) <= ?"
                            params.append(date_to_obj.isoformat())
                        except ValueError:
                            logger.warning(f"Неверный формат даты: {filters['date_to']}")
                    
                    if filters.get("start_date"):
                        try:
                            start_date_obj = datetime.strptime(filters["start_date"], "%Y-%m-%d").date()
                            query += " AND DATE(upload_date) >= ?"
                            params.append(start_date_obj.isoformat())
                        except ValueError:
                            logger.warning(f"Неверный формат даты: {filters['start_date']}")
                    
                    if filters.get("end_date"):
                        try:
                            end_date_obj = datetime.strptime(filters["end_date"], "%Y-%m-%d").date()
                            query += " AND DATE(upload_date) <= ?"
                            params.append(end_date_obj.isoformat())
                        except ValueError:
                            logger.warning(f"Неверный формат даты: {filters['end_date']}")
                
                query += " ORDER BY upload_date DESC"
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                documents = [self._row_to_document(row) for row in rows]
                logger.info(f"Найдено документов: {len(documents)}")
                return documents
                
        except Exception as e:
            logger.error(f"Ошибка получения документов: {e}")
            return []
    
    def update_document(self, doc_id: int, updated_fields: Dict[str, Any]) -> bool:
        """Обновление документа"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Получаем текущий документ
                cursor.execute("SELECT fields FROM documents WHERE id = ?", (doc_id,))
                row = cursor.fetchone()
                
                if not row:
                    return False
                
                # Обновляем поля
                current_fields = json.loads(row[0])
                
                for field in current_fields:
                    if field["name"] in updated_fields:
                        field["value"] = str(updated_fields[field["name"]])
                
                # Сохраняем обновленные поля
                updated_fields_json = json.dumps(current_fields)
                
                cursor.execute("""
                    UPDATE documents 
                    SET fields = ?, validation_errors = NULL
                    WHERE id = ?
                """, (updated_fields_json, doc_id))
                
                conn.commit()
                logger.info(f"Документ {doc_id} обновлен")
                return True
                
        except Exception as e:
            logger.error(f"Ошибка обновления документа: {e}")
            return False
    
    def get_document_for_api(self, doc_id: int) -> Optional[Dict[str, Any]]:
        """Получение документа в формате для API"""
        try:
            doc = self.get_document(doc_id)
            if not doc:
                return None
            
            # Преобразуем в формат для API
            return {
                "id": doc.id,
                "filename": doc.filename,
                "document_type": doc.doc_type,
                "processing_date": doc.upload_date.isoformat() if doc.upload_date else "",
                "confidence": doc.confidence,
                "extracted_data": {field.name: field.value for field in doc.fields},
                "is_valid": len(doc.validation_errors or []) == 0,
                "validation_errors": doc.validation_errors or [],
                "file_path": doc.file_path
            }
            
        except Exception as e:
            logger.error(f"Ошибка получения документа для API: {e}")
            return None 