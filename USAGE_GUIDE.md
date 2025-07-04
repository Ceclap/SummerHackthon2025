# 📖 Руководство по использованию AI Помощника Бухгалтера

## 🎯 Обзор новой структуры

Проект теперь организован согласно сценарию:

```
/
├── 📄 Загрузить документ
│   └── 🔍 Распознать
├── ✅ Проверка и исправление
│   └── ✏️ Редактировать → 📥 Скачать
├── 📁 Архив
│   └── 🔍 Поиск, 📊 Экспорт, 📈 Графики
```

## 🚀 Пошаговое руководство

### 1. 📄 Загрузить документ

#### Шаг 1: Откройте приложение
- Перейдите по адресу: `http://localhost:8000`
- Вы увидите главную страницу с тремя вкладками

#### Шаг 2: Загрузите документ
- Нажмите на вкладку **"📄 Загрузить документ"**
- Перетащите файл в область загрузки или нажмите для выбора
- Поддерживаемые форматы: PDF, JPG, PNG, TIFF
- Максимальный размер: 50MB

#### Шаг 3: Дождитесь обработки
- Система автоматически:
  - Распознает тип документа
  - Извлечет данные с помощью OCR и AI
  - Покажет результат с уверенностью

#### Пример результата:
```
✅ Документ успешно распознан!
Тип документа: factura_fiscala
Уверенность: 95.2%
Извлеченные поля:
- Номер: F-2025-001
- Дата: 2025-01-15
- Продавец: SRL "AlfaCom"
- Покупатель: SRL "BetaCorp"
- IDNO: 1007600000001
- Сумма: 15000.00 L
- НДС: 3000.00 L
```

### 2. ✅ Проверка и исправление

#### Шаг 1: Перейдите к проверке
- Нажмите на вкладку **"✅ Проверка и исправление"**
- Система покажет все документы, требующие проверки

#### Шаг 2: Выберите документ
- В списке найдите нужный документ
- Нажмите **"✏️ Редактировать"**

#### Шаг 3: Отредактируйте данные
- В открывшемся модальном окне проверьте все поля
- Исправьте ошибки в распознавании
- Нажмите **"Сохранить"**

#### Шаг 4: Скачайте результат
- После сохранения нажмите **"📥 Скачать"**
- Документ будет сохранен в вашей системе

### 3. 📁 Архив

#### Шаг 1: Откройте архив
- Нажмите на вкладку **"📁 Архив"**
- Здесь вы найдете все обработанные документы

#### Шаг 2: Поиск документов
Используйте фильтры для поиска:
- **Поиск по тексту**: Введите ключевые слова
- **Тип документа**: Выберите из списка
- **Дата от/до**: Укажите период
- Нажмите **"🔍 Поиск"**

#### Шаг 3: Экспорт данных
- Нажмите **"📊 Экспорт"**
- Выберите формат: JSON, Excel, CSV
- Файл автоматически скачается

#### Шаг 4: Просмотр графиков
- Нажмите **"📈 Графики"**
- Увидите статистику по типам документов
- Анализ объема документов по месяцам

## 🔧 Полезные функции

### Drag & Drop загрузка
- Просто перетащите файл в область загрузки
- Система автоматически начнет обработку

### Автоматическое распознавание
- AI определяет тип документа с высокой точностью
- Извлекает все ключевые поля
- Проверяет валидность данных

### Умная валидация
- Проверка формата IDNO (13 цифр)
- Валидация дат
- Проверка сумм и НДС
- Выявление ошибок и несоответствий

### Гибкий поиск
- Поиск по содержимому документа
- Фильтрация по типу и дате
- Комбинированные фильтры

## 📊 Типы документов

Система поддерживает следующие типы молдавских документов:

1. **Счет-фактура (Factura Fiscală)**
   - Номер, дата, стороны
   - IDNO, суммы, НДС

2. **Фискальный чек (Bon Fiscal)**
   - Товары, количества, цены
   - Итоговая сумма

3. **Контракт (Contract)**
   - Стороны, предмет, условия
   - Сроки, обязательства

4. **Квитанция (Chitanță)**
   - Номер, дата, сумма
   - Назначение платежа

5. **Накладная (Aviz de însoțire)**
   - Товары, количества
   - Отправитель, получатель

6. **Счет (Factură)**
   - Услуги, работы
   - Суммы, условия

7. **Декларация (Declarație)**
   - Период, данные
   - Суммы, расчеты

8. **Другие документы**
   - Автоматическое распознавание
   - Извлечение доступных полей

## 🎨 Интерфейс

### Современный дизайн
- Адаптивная верстка
- Красивые градиенты
- Анимации и переходы
- Интуитивная навигация

### Цветовая схема
- Основной: Сине-фиолетовый градиент
- Успех: Зеленый
- Предупреждение: Желтый
- Ошибка: Красный

### Иконки
- 📄 Документы
- ✅ Проверка
- 📁 Архив
- 🔍 Поиск
- 📊 Экспорт
- 📈 Графики

## 🔍 Поиск и фильтрация

### Текстовый поиск
- Поиск по названию файла
- Поиск по содержимому документа
- Нечеткий поиск

### Фильтры по типу
- Все типы
- Счет-фактура
- Контракт
- Квитанция

### Фильтры по дате
- Дата от
- Дата до
- Период

### Комбинированные фильтры
- Можно использовать несколько фильтров одновременно
- Результаты обновляются в реальном времени

## 📈 Экспорт и отчеты

### Форматы экспорта
- **JSON**: Для интеграции с системами
- **Excel**: Для бухгалтерии
- **CSV**: Для анализа данных

### Типы отчетов
- **Сводный отчет**: Общая статистика
- **Детальный отчет**: По каждому документу
- **Фискальный отчет**: Для налоговой службы

### Автоматическое форматирование
- Стилизованные таблицы
- Заголовки и подписи
- Цветовое оформление

## 🛠 Советы и рекомендации

### Для лучшего распознавания
1. Используйте качественные изображения
2. Убедитесь в хорошем освещении
3. Документ должен быть ровным
4. Текст должен быть четким

### Для быстрой работы
1. Используйте drag & drop
2. Проверяйте документы сразу после загрузки
3. Используйте фильтры для поиска
4. Экспортируйте данные регулярно

### Для точности данных
1. Всегда проверяйте распознанные данные
2. Исправляйте ошибки сразу
3. Используйте валидацию системы
4. Сохраняйте историю изменений

## 🆘 Решение проблем

### Документ не загружается
- Проверьте размер файла (максимум 50MB)
- Убедитесь в поддерживаемом формате
- Проверьте подключение к интернету

### Ошибки распознавания
- Попробуйте улучшить качество изображения
- Проверьте ориентацию документа
- Убедитесь в четкости текста

### Проблемы с поиском
- Проверьте правильность фильтров
- Убедитесь в корректности дат
- Попробуйте более широкие критерии

### Ошибки экспорта
- Проверьте доступ к папке загрузок
- Убедитесь в достаточном месте на диске
- Попробуйте другой формат экспорта

## 📞 Поддержка

При возникновении проблем:

1. **Проверьте логи**: `logs/app.log`
2. **Перезапустите сервер**: `python run.py`
3. **Проверьте настройки**: Файл `.env`
4. **Обратитесь к документации**: README.md

---

**Версия руководства**: 2.0.0  
**Дата обновления**: 2025-06-21 