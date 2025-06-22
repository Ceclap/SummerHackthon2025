import os
import openai
import json
import traceback
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file, g
from flask_babel import Babel, _
from werkzeug.utils import secure_filename
import base64
import openpyxl
from io import BytesIO
from dotenv import load_dotenv
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError
import mimetypes
from datetime import datetime

# Загружаем переменные окружения из .env файла
load_dotenv()

# --- Настройка клиента OpenAI ---
# Создаем единый клиент, который будет использоваться во всем приложении
client = None
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    try:
        client = openai.OpenAI(api_key=api_key)
        # Проверяем подключение
        client.models.list()
        print("✅ OpenAI API успешно подключен")
    except Exception as e:
        print(f"⚠️  Ошибка подключения к OpenAI API: {e}")
        client = None
else:
    print("⚠️  OPENAI_API_KEY не найден в .env файле")

# --- Конфигурация Flask ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a-very-secret-key-that-should-be-changed')
app.config['BABEL_DEFAULT_LOCALE'] = 'ro'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

LANGUAGES = {'en': 'English', 'ro': 'Română', 'ru': 'Русский'}
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'gif', 'webp'}


# --- Настройка Babel для локализации ---
def get_locale():
    # Попробовать получить язык из сессии
    language = session.get('language')
    if language:
        return language
    # В противном случае, использовать лучший выбор из заголовков accept-languages
    return request.accept_languages.best_match(LANGUAGES.keys())

babel = Babel(app, locale_selector=get_locale)


# --- Маршруты (Routes) ---

@app.before_request
def before_request():
    g.locale = get_locale()


@app.route('/set_language/<lang>')
def set_language(lang):
    """Маршрут для смены языка."""
    if lang in LANGUAGES:
        session['language'] = lang
    # Перенаправляем пользователя на ту же страницу, где он был
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/')
def index():
    recent_documents = session.get('recent_documents', [])
    return render_template('index.html', recent_documents=recent_documents)

@app.route('/dashboard')
def dashboard():
    return redirect(url_for('index', _anchor='dashboard'))

@app.route('/incarcare')
def incarcare():
    """Страница загрузки и обработки документов."""
    return render_template('incarcare.html')

@app.route('/tipuri-de-documente')
def tipuri_de_documente():
    """Страница с типами документов (заглушка)."""
    # Mock data
    doc_types = {
        "FF": {"name": "Factura Fiscală", "initial": "F", "color": "#3f51b5", "docs": [{"id": "FF-2023-08-15-001", "date": "15.08.2023"}]},
        "BF": {"name": "Bon Fiscal", "initial": "B", "color": "#4caf50", "docs": [{"id": "BF-2023-08-15-012", "date": "15.08.2023"}]}
    }
    return render_template('tipuri_de_documente.html', doc_types=doc_types)


# --- API Роуты ---

@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        flash(_('Файл не выбран'), 'error')
        return redirect(url_for('incarcare'))
    
    file = request.files['file']
    if file.filename == '':
        flash(_('Файл не выбран'), 'error')
        return redirect(url_for('incarcare'))

    if not allowed_file(file.filename):
        flash(_('Неподдерживаемый тип файла. Поддерживаются: PNG, JPG, JPEG, PDF, GIF, WEBP'), 'error')
        return redirect(url_for('incarcare'))

    # Проверяем размер файла
    file.seek(0, 2)  # Перемещаемся в конец файла
    file_size = file.tell()
    file.seek(0)  # Возвращаемся в начало
    
    if file_size > app.config['MAX_CONTENT_LENGTH']:
        flash(_('Файл слишком большой. Максимальный размер: 16MB'), 'error')
        return redirect(url_for('incarcare'))

    if not client:
        flash(_('AI-функции временно недоступны. Пожалуйста, попробуйте позже.'), 'warning')
        return redirect(url_for('incarcare'))

    if file:
        try:
            # Убедимся, что папка для загрузок существует
            upload_folder = app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            file_ext = os.path.splitext(filename)[1].lower()
            mime_type = "image/jpeg" # По умолчанию
            image_bytes = None

            if file_ext == '.pdf':
                try:
                    # Конвертируем первую страницу PDF в изображение
                    pages = convert_from_path(filepath, 1, fmt='jpeg')
                    if pages:
                        # Сохраняем изображение во временный буфер в памяти
                        buffer = BytesIO()
                        pages[0].save(buffer, format="JPEG")
                        image_bytes = buffer.getvalue()
                        mime_type = "image/jpeg"
                    else:
                        flash(_('Не удалось обработать PDF файл'), 'error')
                        return redirect(url_for('incarcare'))
                except PDFInfoNotInstalledError:
                    flash(_("Для обработки PDF файлов необходимо установить Poppler. На macOS: 'brew install poppler'"), 'error')
                    return redirect(url_for('incarcare'))
                except Exception as e:
                    flash(_('Ошибка при обработке PDF файла'), 'error')
                    return redirect(url_for('incarcare'))
            else:
                # Для обычных изображений
                mime_type = mimetypes.guess_type(filepath)[0] or 'application/octet-stream'
                with open(filepath, "rb") as image_file:
                    image_bytes = image_file.read()

            if not image_bytes:
                flash(_("Не удалось обработать файл"), 'error')
                return redirect(url_for('incarcare'))

            base64_image = base64.b64encode(image_bytes).decode('utf-8')

            prompt = _("Извлеки данные из этой таблицы в формате JSON. В ответе должен быть список объектов, где каждый объект - это строка, а ключи - это заголовки столбцов. Например: [{\"Колонка1\": \"Значение1\", \"Колонка2\": \"Значение2\"}]. Верни только JSON без какого-либо дополнительного текста или объяснений.")
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}}
                        ],
                    }],
                    max_tokens=3000,
                    response_format={"type": "json_object"}
                )
            except Exception as e:
                print(f"Ошибка при вызове OpenAI API: {e}")
                flash(_('Ошибка при обработке изображения через AI. Пожалуйста, попробуйте позже.'), 'error')
                return redirect(url_for('incarcare'))

            if response.choices[0].message.content:
                try:
                    json_data = json.loads(response.choices[0].message.content)
                    
                    # OpenAI может вернуть JSON с одним ключом, значение которого - список таблиц
                    if isinstance(json_data, dict) and len(json_data.keys()) == 1:
                        table_key = list(json_data.keys())[0]
                        extracted_data = json_data[table_key]
                    else:
                        extracted_data = json_data

                    if not isinstance(extracted_data, list):
                        raise ValueError("JSON data is not a list of objects.")

                    # --- Новый шаг: Интеллектуальная классификация ---
                    try:
                        metadata = get_document_metadata(extracted_data)
                    except Exception as e:
                        print(f"Ошибка при получении метаданных: {e}")
                        metadata = {}

                    session['extracted_data'] = extracted_data
                    session['filename'] = filename
                    session['image_url'] = url_for('static', filename=f'uploads/{filename}')

                    if 'recent_documents' not in session:
                        session['recent_documents'] = []
                    
                    doc_type = metadata.get('document_type', _('Неизвестный тип'))
                    doc_id = metadata.get('document_number', f'file-{datetime.now().strftime("%H%M%S")}')
                    doc_date = metadata.get('document_date', datetime.now().strftime('%d.%m.%Y'))

                    new_doc = {
                        'filename': filename,
                        'document_type': doc_type,
                        'document_number': doc_id,
                        'document_date': doc_date,
                        'status': _('Procesat') # Processed
                    }

                    recent_docs = session.get('recent_documents', [])
                    recent_docs.insert(0, new_doc)
                    session['recent_documents'] = recent_docs[:10]  # Храним только последние 10

                    flash(_('Документ успешно обработан!'), 'success')
                    return redirect(url_for('result', filename=filename))

                except json.JSONDecodeError:
                    flash(_('Ошибка при обработке данных из изображения'), 'error')
                    return redirect(url_for('incarcare'))
                except Exception as e:
                    print(f"Неожиданная ошибка при обработке данных: {e}")
                    flash(_('Неожиданная ошибка при обработке данных'), 'error')
                    return redirect(url_for('incarcare'))
            else:
                flash(_('Не удалось извлечь данные из изображения'), 'error')
                return redirect(url_for('incarcare'))

        except Exception as e:
            print(f"Ошибка при обработке файла: {e}")
            flash(_('Ошибка при обработке файла'), 'error')
            return redirect(url_for('incarcare'))
    
    flash(_('Ошибка при загрузке файла'), 'error')
    return redirect(url_for('incarcare'))

@app.route('/result/<filename>')
def result(filename):
    # Получаем данные из сессии
    table_data = session.get('extracted_data', [])
    image_url = url_for('static', filename=f'uploads/{filename}')
    
    # Проверяем, что файл действительно существует, чтобы избежать ошибок
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        flash(_('Файл не найден.'))
        return redirect(url_for('dashboard'))

    return render_template('result.html', table_data=table_data, filename=filename, image_url=image_url)

@app.route('/download/<filename>', methods=['POST'])
def download(filename):
    try:
        # Получаем отредактированные данные из тела запроса
        edited_data = request.get_json()

        # Создаем DataFrame с помощью Pandas
        df = pd.DataFrame(edited_data)
        
        # Создаем Excel файл в памяти
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)

        # Формируем имя нового файла
        base_filename, file_extension = os.path.splitext(filename)
        excel_filename = f"{base_filename}_edited.xlsx"

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=excel_filename
        )

    except Exception as e:
        print(f"Error creating Excel file: {e}")
        return "Error creating file", 500

@app.route('/ask_ai', methods=['POST'])
def ask_ai():
    try:
        data = request.get_json()
        question = data.get('question', '')
        if not question:
            return jsonify({'answer': 'Пожалуйста, введите вопрос.'}), 400

        # Здесь ваш код обращения к OpenAI
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты ИИ-ассистент бухгалтерии и сайта ContaSfera. Отвечай на вопросы по сайту, бухгалтерии и законам Молдовы простым языком."},
                {"role": "user", "content": question}
            ],
            max_tokens=500
        )
        answer = response.choices[0].message.content.strip()
        print(f"AI ответ: {answer}")  # Логируем ответ
        return jsonify({'answer': answer})

    except Exception as e:
        print(f"Ошибка в /ask_ai: {e}")
        return jsonify({'answer': f'Ошибка: {str(e)}'}), 500

@app.route('/classify', methods=['POST'])
def classify():
    """Классификация документа: определение типа, номера, даты."""
    if 'file' not in request.files:
        return jsonify({'error': _('Файл не выбран')}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': _('Файл не выбран')}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': _('Неподдерживаемый тип файла')}), 400
    if not client:
        return jsonify({'error': _('AI-функции временно недоступны.')}), 503
    # Сохраняем файл во временную папку
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    # Обработка файла (pdf->jpeg, image->bytes)
    file_ext = os.path.splitext(filename)[1].lower()
    mime_type = mimetypes.guess_type(filepath)[0] or 'application/octet-stream'
    image_bytes = None
    if file_ext == '.pdf':
        pages = convert_from_path(filepath, 1, fmt='jpeg')
        if pages:
            buffer = BytesIO()
            pages[0].save(buffer, format="JPEG")
            image_bytes = buffer.getvalue()
            mime_type = "image/jpeg"
        else:
            return jsonify({'error': _('Не удалось обработать PDF файл')}), 400
    else:
        with open(filepath, "rb") as image_file:
            image_bytes = image_file.read()
    if not image_bytes:
        return jsonify({'error': _('Не удалось обработать файл')}), 400
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    prompt = _("Определи тип, номер и дату документа на изображении. Верни JSON с ключами document_type, document_number, document_date.")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}}
                ],
            }],
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        metadata = json.loads(response.choices[0].message.content)
        return jsonify(metadata)
    except Exception as e:
        print(f"Ошибка в /classify: {e}")
        return jsonify({'error': _('Ошибка при обращении к AI')}), 500

@app.route('/convert', methods=['POST'])
def convert():
    """Конвертация фото/скана в таблицу (json) и Excel."""
    if 'file' not in request.files:
        return jsonify({'error': _('Файл не выбран')}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': _('Файл не выбран')}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': _('Неподдерживаемый тип файла')}), 400
    if not client:
        return jsonify({'error': _('AI-функции временно недоступны.')}), 503
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    file_ext = os.path.splitext(filename)[1].lower()
    mime_type = mimetypes.guess_type(filepath)[0] or 'application/octet-stream'
    image_bytes = None
    if file_ext == '.pdf':
        pages = convert_from_path(filepath, 1, fmt='jpeg')
        if pages:
            buffer = BytesIO()
            pages[0].save(buffer, format="JPEG")
            image_bytes = buffer.getvalue()
            mime_type = "image/jpeg"
        else:
            return jsonify({'error': _('Не удалось обработать PDF файл')}), 400
    else:
        with open(filepath, "rb") as image_file:
            image_bytes = image_file.read()
    if not image_bytes:
        return jsonify({'error': _('Не удалось обработать файл')}), 400
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    prompt = _("Извлеки таблицу из этого изображения в формате JSON. Верни только JSON.")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}}
                ],
            }],
            max_tokens=3000,
            response_format={"type": "json_object"}
        )
        json_data = json.loads(response.choices[0].message.content)
        # Сохраняем для скачивания Excel
        session['converted_data'] = json_data
        session['converted_filename'] = filename
        return jsonify({'table': json_data, 'filename': filename})
    except Exception as e:
        print(f"Ошибка в /convert: {e}")
        return jsonify({'error': _('Ошибка при обращении к AI')}), 500

@app.route('/convert/download', methods=['GET'])
def download_converted():
    """Скачивание Excel-файла после конвертации."""
    data = session.get('converted_data')
    filename = session.get('converted_filename', 'converted.xlsx')
    if not data:
        return "Нет данных для скачивания", 400
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    excel_filename = f"{os.path.splitext(filename)[0]}_converted.xlsx"
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=excel_filename
    )

@app.route('/check', methods=['POST'])
def check():
    """Проверка документа (json-таблицы) на ошибки/подлинность."""
    data = request.get_json()
    if not data:
        return jsonify({'error': _('Нет данных для проверки')}), 400
    prompt = _("Проверь эту таблицу на ошибки, подозрительные значения и соответствие законодательству Молдовы. Верни список найденных проблем или 'OK', если всё хорошо.")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"{prompt}\n{json.dumps(data)}"}],
            max_tokens=1000
        )
        result = response.choices[0].message.content
        return jsonify({'result': result})
    except Exception as e:
        print(f"Ошибка в /check: {e}")
        return jsonify({'error': _('Ошибка при обращении к AI')}), 500

@app.route('/assistant', methods=['POST'])
def assistant():
    """ИИ-ассистент по закону Молдовы и использованию сайта."""
    if not client:
        return jsonify({'error': _('AI-функции временно недоступны.')}), 503
    question = request.json.get('question')
    if not question:
        return jsonify({'error': _('Вопрос не был предоставлен.')}), 400
    try:
        with open('system_prompt.txt', 'r', encoding='utf-8') as f:
            system_prompt_template = f.read()
        current_language_name = LANGUAGES.get(get_locale(), 'English')
        system_prompt = system_prompt_template.format(current_language=current_language_name)
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=1000,
            temperature=0.5
        )
        answer = completion.choices[0].message.content
        return jsonify({'answer': answer})
    except Exception as e:
        print(f"Ошибка в /assistant: {e}")
        return jsonify({'error': _('Ошибка при обращении к AI')}), 500

@app.route('/archive')
def archive():
    """Архив документов: просмотр и скачивание загруженных файлов."""
    files = []
    upload_folder = app.config['UPLOAD_FOLDER']
    if os.path.exists(upload_folder):
        for fname in os.listdir(upload_folder):
            fpath = os.path.join(upload_folder, fname)
            if os.path.isfile(fpath):
                files.append({
                    'filename': fname,
                    'url': url_for('static', filename=f'uploads/{fname}')
                })
    return render_template('archive.html', files=files)

# --- Вспомогательные функции ---

def allowed_file(filename):
    """Проверяет, разрешен ли тип файла."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_document_metadata(data: list) -> dict:
    """Возвращает метаданные (тип, номер, дата) из текста документа."""
    if not client:
        return {}

    # Преобразуем список словарей в более простую строку для анализа
    text_data = ""
    for row in data:
        text_data += " | ".join(str(v) for v in row.values()) + "\\n"
    
    prompt = f"""
Проанализируй следующие данные, извлеченные из таблицы, и определи Тип документа, Номер документа и Дату документа.
Данные:
{text_data}

Верни ответ в формате JSON с ключами "document_type", "document_number", "document_date".
Например: {{"document_type": "Factura Fiscala", "document_number": "FF2023001", "document_date": "15.08.2023"}}
Если какая-то информация отсутствует, используй "N/A".
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            response_format={"type": "json_object"}
        )
        metadata = json.loads(response.choices[0].message.content)
        return metadata
    except Exception as e:
        print(f"Error getting document metadata: {e}")
        return {}

if __name__ == '__main__':
    # Убедимся, что папка для загрузок существует
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5001)
