import json
import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, date
from dataclasses import dataclass, asdict
from pathlib import Path
import sqlite3
from document_classifier import DocumentData, DocumentField

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
                        date_from: Optional[date] = None,
                        date_to: Optional[date] = None,
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
                    query += " AND DATE(upload_date) >= ?"
                    params.append(date_from.isoformat())
                
                if date_to:
                    query += " AND DATE(upload_date) <= ?"
                    params.append(date_to.isoformat())
                
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
    
    def get_statistics(self, month: Optional[int] = None, year: Optional[int] = None) -> Dict[str, Any]:
        """Получает статистику по документам"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Общая статистика
                cursor.execute("SELECT COUNT(*) FROM documents")
                total_docs = cursor.fetchone()[0]
                
                # Статистика по типам документов
                cursor.execute("""
                    SELECT doc_type, COUNT(*) as count 
                    FROM documents 
                    GROUP BY doc_type
                """)
                type_stats = dict(cursor.fetchall())
                
                # Статистика по месяцам
                if month and year:
                    cursor.execute("""
                        SELECT doc_type, COUNT(*) as count 
                        FROM documents 
                        WHERE strftime('%m', upload_date) = ? AND strftime('%Y', upload_date) = ?
                        GROUP BY doc_type
                    """, (f"{month:02d}", str(year)))
                    monthly_stats = dict(cursor.fetchall())
                else:
                    monthly_stats = {}
                
                # Подсчет общих сумм (требует парсинга полей)
                total_amounts = {}
                cursor.execute("SELECT doc_type, fields FROM documents")
                for row in cursor.fetchall():
                    doc_type = row[0]
                    fields_json = row[1]
                    try:
                        fields = json.loads(fields_json)
                        amount_fields = [f for f in fields if "amount" in f["name"]]
                        if amount_fields:
                            amount = float(amount_fields[0]["value"].replace(",", ""))
                            total_amounts[doc_type] = total_amounts.get(doc_type, 0) + amount
                    except (json.JSONDecodeError, ValueError, KeyError):
                        continue
                
                return {
                    "total_documents": total_docs,
                    "by_type": type_stats,
                    "monthly_stats": monthly_stats,
                    "total_amounts": total_amounts
                }
                
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return {}
    
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
            
            return StoredDocument(
                id=row[0],
                filename=row[1],
                doc_type=row[2],
                fields=fields,
                raw_text=row[4],
                upload_date=datetime.fromisoformat(row[5]),
                file_path=row[6],
                confidence=row[7],
                validation_errors=validation_errors,
                validation_warnings=validation_warnings
            )
        except Exception as e:
            logger.error(f"Ошибка преобразования строки в документ: {e}")
            raise 