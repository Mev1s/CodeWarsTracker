# 🏆 Codewars Tracker

Telegram-бот и REST API для отслеживания статистики Codewars. Автоматически парсит профиль пользователя, сохраняет статистику и позволяет сравнивать прогресс с другими участниками.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Telegram Bot](https://img.shields.io/badge/Telegram_Bot-4.14-blue)

## ✨ Возможности

### 🤖 Telegram Bot
- `/start` — начать работу с ботом
- `/nick username` — установить/изменить никнейм Codewars
- `/stats` — посмотреть текущую статистику
- `/change_nick username` — изменить никнейм
- `/leaders` — топ-10 пользователей по чести
- `/help` — справка по командам

### 🌐 REST API (FastAPI)
- `GET /users` — список всех пользователей
- `GET /users/{id}` — информация о конкретном пользователе
- `POST /users` — создать нового пользователя
- `GET /user_stats` — вся статистика пользователей
- Автоматическая документация: `http://localhost:8000/docs`

## 📦 Технологии

- **Backend:** FastAPI, SQLAlchemy, Pydantic, Psycopg2
- **Database:** PostgreSQL
- **Bot:** python-telegram-bot (telebot)
- **Parsing:** BeautifulSoup4, Requests