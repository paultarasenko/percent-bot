# 📊 Процентный калькулятор — Telegram Bot

Telegram-бот для быстрого расчёта процентов. Простой интерфейс, мгновенные результаты.

## Скриншоты

![Bot Screenshot](docs/screenshot.png)

## Возможности

**📊 % от числа**
> 12% от 2000 = 240

**🔢 Найти процент**
> 100 из 2000 = 5%

**📈 Изменение в %**
> 20 → 100 = +400%

**🏦 Кредитный калькулятор**
> Сумма, ставка, срок → ежемесячный платёж и переплата

**💰 Вклад в банке**
> Без капитализации и с капитализацией

## Технологии

- Python 3.12
- aiogram 3.x
- FSM (Finite State Machine)
- pydantic-settings
- Logging
- Type Hints
- Modular Architecture
- Деплой: Railway

## Структура проекта

```
percent_bot/
├── bot.py              # точка входа
├── config.py           # настройки из .env
├── requirements.txt
├── .env.example
│
├── handlers/           # обработчики сообщений и callback
├── keyboards/          # inline-клавиатуры
├── services/           # математика (чистые функции)
├── states/             # FSM states
├── texts/              # все строки интерфейса
├── utils/              # форматирование и валидация
└── logs/
```

## Запуск локально

```bash
# 1. Клонируй репозиторий
git clone https://github.com/paultarasenko/percent-bot.git
cd percent-bot

# 2. Создай виртуальное окружение
python -m venv venv

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Windows (Git Bash):
source venv/Scripts/activate

# macOS / Linux:
source venv/bin/activate

# 3. Установи зависимости
pip install -r requirements.txt

# 4. Создай .env
cp .env.example .env
# вставь токен бота в BOT_TOKEN

# 5. Запусти
python bot.py
```

## Деплой на Railway

1. Залей проект на GitHub
2. В Railway: **New Project → Deploy from GitHub repo**
3. Добавь переменную окружения: `BOT_TOKEN=твой_токен`
4. Railway запустит бота автоматически

## Переменные окружения

| Переменная | Описание | По умолчанию |
|---|---|---|
| `BOT_TOKEN` | Токен от @BotFather | обязательно |
| `LOG_LEVEL` | Уровень логирования | `INFO` |
| `USE_WEBHOOK` | Webhook вместо polling | `false` |
| `WEBHOOK_HOST` | URL для webhook | — |
| `WEBHOOK_PATH` | Путь для webhook | `/webhook` |
| `WEBHOOK_PORT` | Порт для webhook | `8080` |

## Лицензия

MIT License

## Автор

[@paultarasenko](https://github.com/paultarasenko)
