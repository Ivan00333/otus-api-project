# API Automation Framework for Reqres.in

Автоматизированный фреймворк для тестирования HTTP API сервиса Reqres.in ([https://reqres.in/](https://reqres.in/)).

## Описание

Проект реализует автотесты для основных сценариев работы с ресурсами `/users` и `/register`. Он покрывает создание, получение, обновление и удаление пользователей, а также позитивные и негативные случаи регистрации.

### Основные возможности

Поддержка retry-политики при сетевых ошибках.
Генерация подробных Allure-отчётов с шагами и вложениями.
Параметризация запуска тестов на разных ветках через Jenkins Pipeline.

## Технологический стек

Язык: Python 3.13
HTTP-клиент: requests и urllib3 с поддержкой retry
Валидация и модели: pydantic и pydantic-settings
Тестовый фреймворк: pytest с расширениями pytest-xdist и pytest-cov
Отчёты: allure-pytest и Allure CLI
CI/CD: Jenkins Pipeline

## Предварительные требования

Для работы необходимы установленные Python 3.13, pip, Git и Jenkins с плагином Allure Report.

## Установка и настройка локально

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/your-org/your-repo.git
   cd your-repo
   ```
2. Создайте и активируйте виртуальное окружение:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # для Windows PowerShell: .\.venv\Scripts\Activate.ps1
   ```
3. Установите зависимости:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Задайте базовый URL через переменную окружения:

   ```bash
   export USERS_CLIENT__URL=https://reqres.in/api/
   # для Windows PowerShell:
   # $Env:USERS_CLIENT__URL = 'https://reqres.in/api/'
   ```

## Структура проекта

```
├── api/
│   ├── base_client.py         # HTTP-клиент с retry, логированием и шагами Allure
│   └── users_client.py        # Методы для работы с /users и /register
├── models/
│   ├── user_request_model.py  # Pydantic-схемы запросов
│   ├── user_response_model.py # Pydantic-схемы ответов
│   └── auth_model.py          # Схемы для регистрации
├── assertions/
│   └── base_assertions.py     # Утилиты для проверок
├── tests/
│   ├── test_get_users.py
│   ├── test_get_single_user.py
│   ├── test_create_user.py
│   ├── test_update_user.py
│   ├── test_delete_user.py
│   └── test_register_user.py
├── pytest.ini                 # Настройки pytest и Allure
├── requirements.txt           # Список Python-зависимостей
├── Dockerfile.jenkins         # Dockerfile для Jenkins-агента с Python3
├── Jenkinsfile                # Пайплайн для CI: параметр BRANCH и публикация Allure
└── README.md                  # Документация проекта
```

## Запуск тестов локально

```bash
pytest --clean-alluredir --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## Jenkins Pipeline

Файл Jenkinsfile параметризован по ветке BRANCH и включает этапы:
— Checkout указанной ветки из Git
— Создание виртуального окружения и установка зависимостей
— Запуск pytest с генерацией Allure-результатов
— Публикация отчёта из папки allure-results

При сборке в интерфейсе Jenkins появится кнопка Allure Report.

## Вклад и развитие

Чтобы внести изменения, создайте форк репозитория, новую ветку именем `feature/...`, добавьте улучшения и откройте Pull Request для review.

© 2025 API Automation Framework для Reqres.in
