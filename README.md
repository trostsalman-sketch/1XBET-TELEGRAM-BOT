# 1XBET Telegram Bot

Полнофункциональный Telegram-бот для игрового RP-проекта 1XBET.

## Особенности

- Три игры: Баскетбол, Футбол, Фортуна
- Минимальная ставка: 10,000 ₽
- Административная панель
- История ставок
- Статистика игрока
- Система ролей (Owner/Admin)
- Блокировка пользователей
- Логирование действий

## Технологии

- Python 3.11+
- aiogram 3.3.0
- PostgreSQL
- SQLAlchemy 2.0
- Alembic (миграции)

## Установка

### 1. Клонируй репозиторий

\`\`\`bash
git clone https://github.com/your-username/1xbet-telegram-bot.git
cd 1xbet-telegram-bot
\`\`\`

### 2. Создай виртуальное окружение

\`\`\`bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
\`\`\`

### 3. Установи зависимости

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Настрой переменные окружения

\`\`\`bash
cp .env.example .env
\`\`\`

Отредактируй `.env` и укажи:
- `BOT_TOKEN` — токен от @BotFather
- `OWNER_ID` — твой Telegram ID
- `DB_*` — данные подключения к PostgreSQL

### 5. Создай базу данных

\`\`\`bash
createdb xbet
\`\`\`

### 6. Примени миграции

\`\`\`bash
alembic upgrade head
\`\`\`

### 7. Запусти бота

\`\`\`bash
python -m bot.main
\`\`\`

## Команды

### Пользовательские

- `/start` — Регистрация и приветствие
- `/stb <сумма>` — Создать ставку
- `/profile` — Профиль игрока
- `/history` — История ставок
- `/helpp` — Помощь

### Административные

- `/adm` — Открыть админ-панель (только в личных сообщениях)

## Структура проекта

\`\`\`
1xbet-telegram-bot/
├── alembic/           # Миграции БД
├── bot/
│   ├── database/     # Модели и репозитории
│   ├── handlers/     # Обработчики команд
│   ├── keyboards/    # Клавиатуры
│   ├── services/     # Бизнес-логика
│   ├── middleware/   # Middleware
│   ├── filters/      # Фильтры
│   └── utils/        # Утилиты
├── .env.example
├── requirements.txt
└── README.md
\`\`\`

## Лицензия

MIT
