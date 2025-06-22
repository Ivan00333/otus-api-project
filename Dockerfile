# Dockerfile
# Используем легковесный образ Python
FROM python:3.13-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Отключаем буферизацию вывода и отключаем создание виртуальных окружений Poetry
ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Устанавливаем системные зависимости для сборки и работы Poetry
RUN apt-get update \
    && apt-get install -y build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем только файлы, описывающие зависимости, чтобы воспользоваться кэшированием Docker
# - CHANGELOG не затрётся при изменении исходного кода
COPY pyproject.toml poetry.lock /app/

# Устанавливаем Poetry и сразу устанавливаем зависимости проекта
RUN pip install --upgrade pip poetry \
    && poetry install --no-root --no-dev

# Копируем весь исходный код проекта
COPY . /app

# По умолчанию запускаем тесты и генерируем Allure-отчёты
CMD ["pytest", "--clean-alluredir", "--alluredir=allure-results"]
