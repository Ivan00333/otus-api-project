# Автоматизированный фреймворк для Reqres.in

Автоматизированный фреймворк для тестирования API сервиса Reqres.in ([https://reqres.in/](https://reqres.in/)).

## Описание

Проект реализует автотесты для основных сценариев работы с ресурсами `/users` и `/register`:

* Создание, получение, обновление и удаление пользователей
* Позитивные и негативные кейсы регистрации

### Основные возможности

* Поддержка retry-политики при сетевых ошибках
* Генерация подробных Allure-отчётов с шагами и вложениями
* Параметризация запуска тестов на разных ветках через Jenkins Pipeline

## Технологический стек

* **Язык**: Python 3.13
* **HTTP-клиент**: requests и urllib3 (Retry)
* **Валидация и модели**: pydantic и pydantic-settings
* **Тестовый фреймворк**: pytest, pytest-xdist, pytest-cov
* **Отчёты**: allure-pytest, Allure CLI
* **CI/CD**: Jenkins Pipeline

## Предварительные требования

* Python 3.13
* pip
* Git
* Jenkins с плагином Allure Report

## Установка и настройка локально

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/Ivan00333/otus-api-project.git
   cd your-repo
   ```
2. Создайте и активируйте виртуальное окружение:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # Windows PowerShell: .\.venv\Scripts\Activate.ps1
   ```
3. Установите зависимости:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Задайте базовый URL через переменную окружения:

   ```bash
   export USERS_CLIENT__URL=https://reqres.in/api/
   # Windows PowerShell:
   # $Env:USERS_CLIENT__URL='https://reqres.in/api/'
   ```

## Структура проекта

```
├── api
│   ├── base_client.py       # HTTP-клиент с retry, логированием и шагами Allure
│   ├── routes.py            # Определение маршрутов API
│   └── users_client.py      # Методы для работы с /users и /register
├── assertions
│   └── base_assertions.py   # Утилиты для проверок и валидации
├── config.py                # Настройки проекта (Pydantic Settings)
├── conftest.py              # Общие фикстуры pytest
├── Dockerfile.jenkins       # Dockerfile для Jenkins-агента с Python3
├── Jenkinsfile              # Pipeline для CI: выбор ветки и публикация Allure
├── models
│   ├── user_request_model.py  # Pydantic-схемы запросов
│   └── user_response_model.py # Pydantic-схемы ответов
├── pytest.ini               # Конфигурация pytest и Allure
├── README.md                # Документация проекта
├── requirements.txt         # Список Python-зависимостей
├── tests
│   ├── test_create_user.py
│   ├── test_delete_user.py
│   ├── test_get_single_user.py
│   ├── test_get_users.py
│   ├── test_register_user.py
│   └── test_update_user.py
└── utils
    └── logger.py           # Настройка и получение логгера
```

## Запуск тестов локально

```bash
pytest --clean-alluredir --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## Jenkins Pipeline

Файл `Jenkinsfile` параметризован по ветке BRANCH и включает следующие этапы:

* Checkout указанной ветки из Git
* Создание виртуального окружения и установка зависимостей
* Запуск `pytest` с генерацией Allure-результатов
* Публикация отчёта из папки `allure-results`

После завершения сборки в интерфейсе Jenkins появится кнопка **Allure Report**.
