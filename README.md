# ContaSfera - Помощник по бухгалтерии для Молдовы

## Описание
ContaSfera - это интеллектуальное приложение для автоматизации бухгалтерских процессов в Республике Молдова. Приложение использует искусственный интеллект для обработки, классификации и анализа бухгалтерских документов.

## Структура проекта

```
SummerHackthon2025/
├── Back/                    # Бэкенд приложения
│   ├── app.py              # Основной Flask сервер
│   ├── requirements.txt    # Python зависимости
│   ├── babel.cfg          # Конфигурация интернационализации
│   ├── system_prompt.txt  # Системный промпт для OpenAI
│   ├── messages.pot       # Файл переводов
│   ├── uploads/           # Загруженные файлы
│   ├── translations/      # Переводы
│   └── README.md          # Документация бэкенда
├── Front/                  # Фронтенд приложения
│   ├── templates/         # HTML шаблоны
│   ├── static/           # Статические файлы (CSS, JS, изображения)
│   └── README.md         # Документация фронтенда
├── README.md             # Основная документация
├── SETUP.md              # Инструкции по установке
└── .gitignore           # Исключения Git
```

## Основные функции

### 🧾 Обработка документов
- Автоматическое распознавание типов документов
- Извлечение данных из изображений с помощью OpenAI Vision API
- Поддержка форматов: PDF, JPG, PNG, GIF, WEBP

### 🧠 ИИ-ассистент
- Ответы на вопросы по законодательству Молдовы
- Помощь в бухгалтерских вопросах
- Многоязычная поддержка (русский, румынский)

### 📊 Классификация документов
- Factura fiscală (Счет-фактура)
- Bon fiscal (Чек)
- Stat de plată (Ведомость зарплаты)
- Act de achiziție (Акт покупки)
- Ordin de plată (Платежное поручение)
- Raport de avans (Отчет по авансу)

### 🌐 Многоязычность
- Русский язык
- Румынский язык
- Автоматическое переключение языков

## Технологии

### Бэкенд
- **Python 3.11+**
- **Flask** - веб-фреймворк
- **OpenAI API** - искусственный интеллект
- **Flask-Babel** - интернационализация
- **SQLite** - база данных

### Фронтенд
- **HTML5/CSS3**
- **JavaScript (ES6+)**
- **Bootstrap** - UI фреймворк
- **Jinja2** - шаблонизатор

## Быстрый старт

### Установка бэкенда
```bash
cd Back
pip install -r requirements.txt
```

### Настройка OpenAI API
Создайте файл `.env` в папке `Back`:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Запуск приложения
```bash
cd Back
python app.py
```

Приложение будет доступно по адресу: http://localhost:5001

## Документация

- [Документация бэкенда](Back/README.md)
- [Документация фронтенда](Front/README.md)
- [Инструкции по установке](SETUP.md)

## Лицензия

MIT License

## Авторы

Команда SummerHackthon2025 