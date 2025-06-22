# Настройка проекта ContaSfera

## Переменные окружения

Для корректной работы проекта необходимо создать файл `.env` в корневой директории проекта.

### Создание файла .env

1. Создайте файл `.env` в корневой директории проекта
2. Добавьте следующие строки:

```env
# OpenAI API Configuration
# Получите ключ на https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Flask Configuration
SECRET_KEY=your-secret-key-here
```

### Получение ключа OpenAI API

1. Перейдите на https://platform.openai.com/api-keys
2. Войдите в свой аккаунт OpenAI
3. Нажмите "Create new secret key"
4. Скопируйте полученный ключ
5. Вставьте его в файл `.env` вместо `your_openai_api_key_here`

### Пример файла .env

```env
OPENAI_API_KEY=sk-1234567890abcdef1234567890abcdef1234567890abcdef
SECRET_KEY=my-super-secret-key-change-this-in-production
```

### Важные замечания

- **Никогда не коммитьте файл `.env` в Git!** Он уже добавлен в `.gitignore`
- Храните ключи в безопасности
- Для продакшена используйте более сложный SECRET_KEY

После создания файла `.env` с правильным ключом OpenAI, перезапустите сервер:

```bash
source venv/bin/activate
python app.py
``` 