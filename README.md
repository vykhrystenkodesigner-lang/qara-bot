# QARA Bot 🤖

Telegram бот для QARA Wallet Mini App.

## Команды

| Команда | Описание |
|---------|----------|
| /start | Запуск бота, главное меню |
| /wallet | Открыть кошелёк |
| /rates | Курсы криптовалют |
| /card | Управление картой |
| /referral | Реферальная программа |
| /support | Техподдержка |
| /help | Список команд |

## Деплой на Railway

1. Заходишь на railway.app
2. New Project → Deploy from GitHub repo
   (или: New Project → Empty Project → Add Service → GitHub Repo)
3. Загружаешь эти файлы в GitHub репозиторий
4. В Railway: Variables → добавляешь:
   - BOT_TOKEN = твой токен от BotFather
   - WEBAPP_URL = https://твой-сайт.netlify.app
   - ADMIN_ID = твой Telegram ID
5. Deploy → бот живой!

## Локальный запуск

```bash
pip install -r requirements.txt
cp .env.example .env
# Заполни .env своими данными
python bot.py
```

## Структура

```
qara_bot/
├── bot.py           # Основной файл бота
├── requirements.txt # Зависимости
├── Procfile         # Для Railway
├── .env.example     # Пример переменных окружения
└── README.md        # Эта документация
```
