# HeadHunter Database

Этот проект предназначен для сбора и анализа данных о работодателях и вакансиях с использованием базы данных PostgreSQL. Данные извлекаются из API HeadHunter и сохраняются в базе данных для дальнейшего анализа.

## Структура проекта

- `main.py`: Основной файл приложения, который управляет пользовательским интерфейсом и взаимодействует с базой данных.
- `db_create.py`: Скрипты для создания базы данных, таблиц и вставки данных.
- `db_manager.py`: Класс для управления подключением к базе данных и выполнения SQL-запросов.
- `utils.py`: Функции для получения данных о работодателях и вакансиях от API HeadHunter.
- `config.py`: Функция для получения конфигурации подключения к базе данных.
- `constant.py`: Константы для работы с API HeadHunter, такие как URL и ID работодателей.
- `database.ini`: Файл конфигурации для подключения к базе данных PostgreSQL.

## Установка и настройка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Для Windows: .\.venv\Scripts\activate
    ```

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4. Создайте файл `database.ini` в корневой директории проекта и добавьте следующие строки:

    ```ini
    [postgresql]
    host=localhost
    user=postgres
    password="yourpassword"
    port=5432
    ```

   **Замените** `yourpassword` на ваш пароль для PostgreSQL.

5. Убедитесь, что файл `constant.py` настроен правильно:

    ```python
    # constant.py

    HH_URL_EMPLOYERS = "https://api.hh.ru/employers"
    HH_URL_VACANCIES = "https://api.hh.ru/vacancies"
    HH_EMPLOYERS_ID = [
        5600787,   # Employer 1
        1035394,   # Employer 2
        5585118,   # Employer 3
        1429999,   # Employer 4
        9498120,   # Employer 5
        561525,    # Employer 6
        84585,     # Employer 7
        12550,     # Employer 8
        2180,      # Employer 9
        3529,      # Employer 10
    ]
    ```

## Использование

1. Запустите `main.py`:
    ```bash
    python main.py
    ```

2. Следуйте инструкциям на экране для создания базы данных, получения данных от API и выполнения различных операций с данными.

3. От каждой комании запрашивается до 100 вакансий.

## Примеры функций

### Функция `get_employers`

Извлекает информацию о работодателях из API HeadHunter и возвращает список работодателей.

### Функция `get_vacancies`

Получает список вакансий для заданного работодателя, извлекая данные из API HeadHunter.

### Функция `get_all_vacancies`

Извлекает все вакансии для заданных работодателей, объединяя результаты для каждого работодателя.

### Функция `create_database`

Создает новую базу данных PostgreSQL, удаляя её, если она уже существует.

### Функция `create_tables`

Создает таблицы `employers` и `vacancies` в базе данных.

### Функция `insert_employers`

Вставляет данные о работодателях в таблицу `employers`.

### Функция `insert_vacancies`

Вставляет данные о вакансиях в таблицу `vacancies`.

## Документация

### Класс `DBManager`

Класс для работы с базой данных PostgreSQL.

- `__init__(self, db_name, db_config)`: Инициализирует экземпляр класса с настройками базы данных.
- `get_companies_and_vacancies(self)`: Возвращает список компаний и количество вакансий у каждой компании.
- `get_all_vacancies(self)`: Возвращает список всех вакансий с указанием компании, вакансии, зарплаты и ссылки.
- `get_avg_salary(self)`: Возвращает среднюю зарплату по вакансиям.
- `get_vacancies_with_higher_salary(self)`: Возвращает вакансии с зарплатой выше средней.
- `get_vacancies_with_keyword(self, keyword)`: Возвращает вакансии, в названии которых содержится переданное слово.

