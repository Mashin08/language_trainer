# Language Trainer - Тренажер для изучения иностранных слов

![Django](https://img.shields.io/badge/Django-3.2-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-blue)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey)

Веб-приложение для создания и повторения иностранных слов с использованием Django.

## 📌 Основные возможности

- 📚 Создание и управление словарными карточками
- 🗂️ Группировка слов по категориям
- ✅ Отметка выученных слов
- 📊 Статистика прогресса обучения
- 👥 Индивидуальные словари для каждого пользователя
- 🔍 Фильтрация слов по статусу изучения

## 🚀 Установка и запуск

### Предварительные требования
- Python 3.8+
- Django 4.1+

### 1. Клонирование репозитория
```bash
git clone https://github.com/Mashin08/language_trainer.git
cd language_trainer
```

### 2. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
```
### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных
```bash
python manage.py migrate
python manage.py loaddata words/fixtures/base_categories.json
python manage.py loaddata words/fixtures/base_words.json
```
### 5. Запуск
```bash
python manage.py runserver
```

📂 Структура проекта
```bash
language_trainer/
├── words/                  # Основное приложение
│   ├── migrations/         # Миграции базы данных
│   ├── templates/          # HTML шаблоны
│   ├── fixtures/           # Начальные данные
│   ├── models.py           # Модели данных
│   ├── views.py            # Логика представлений
│   └── ...
├── language_trainer/       # Настройки проекта
├── manage.py               # Управляющий скрипт
├── requirements.txt        # Зависимости
└── README.md               # Этот файл

```
