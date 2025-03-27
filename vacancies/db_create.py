from typing import List, Dict, Optional, Any

import psycopg2
from psycopg2 import sql

CREATE_TABLES_REQUESTS = [
    """
    CREATE TABLE IF NOT EXISTS employers (
        employer_id INTEGER PRIMARY KEY,
        employer_name VARCHAR(255) NOT NULL,
        url TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS vacancies (
        id SERIAL PRIMARY KEY,
        vacancy_id INTEGER NOT NULL UNIQUE,
        employer_id INTEGER NOT NULL,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        salary INTEGER,
        url TEXT NOT NULL,
        FOREIGN KEY (employer_id) REFERENCES employers (employer_id) ON DELETE CASCADE
    );
    """
]


def create_database(db_name: str, db_config: Dict[str, str]) -> None:
    """
    Подключается к серверу PostgreSQL и создает новую базу данных, сначала удаляя ее, если она существует.

    Args:
        db_name (str): Название базы данных, которую нужно создать.
        db_config (Dict[str, str]): Конфигурация подключения к PostgreSQL, исключая название базы данных.

    Returns:
        None
    """
    conn = psycopg2.connect(dbname='postgres', **db_config)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(db_name)))
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        print(f"База данных '{db_name}' успешно создана")
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        cur.close()
        conn.close()


def create_tables(db_name: str, db_config: Dict[str, str]) -> None:
    """
    Подключается к базе данных PostgreSQL и создает таблицы employers и vacancies, если они не существуют.

    Args:
        db_name (str): Название базы данных, в которой нужно создать таблицы.
        db_config (Dict[str, str]): Конфигурация подключения к PostgreSQL.

    Returns:
        None
    """
    conn = psycopg2.connect(dbname=db_name, **db_config)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        for request in CREATE_TABLES_REQUESTS:
            cur.execute(request)
        conn.commit()
        print("Таблицы успешно созданы")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def insert_employers(employers: List[Dict[str, Optional[str]]], db_name: str, db_config: Dict[str, str]) -> None:
    """
    Вставляет данные о работодателях в базу данных.

    Args:
        employers (List[Dict[str, Optional[str]]]): Список словарей, где каждый словарь содержит
                                                   'employer_id', 'employer_name' и 'url' работодателя.
        db_name (str): Название базы данных.
        db_config (Dict[str, str]): Конфигурация подключения к PostgreSQL, включая название базы данных.

    Returns:
        None
    """
    conn = psycopg2.connect(dbname=db_name, **db_config)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        for emp in employers:
            cur.execute(
                sql.SQL("INSERT INTO employers (employer_id, employer_name, url) "
                        "VALUES (%s, %s, %s) ON CONFLICT (employer_id) DO NOTHING;"),
                (emp['employer_id'], emp['employer_name'], emp['url'])
            )
        conn.commit()
        print("Данные о работодателях успешно заполнены")
    except Exception as e:
        print(f"Ошибка при заполнении данных о работодателях: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def insert_vacancies(vacancies: List[Dict[str, Optional[Any]]], db_name: str, db_config: Dict[str, str]) -> None:
    """
    Вставляет данные о вакансиях в базу данных.

    Args:
        vacancies (List[Dict[str, Optional[Any]]]): Список словарей, где каждый словарь содержит
                                                   'vacancy_id', 'employer_id', 'name', 'description',
                                                   'salary' и 'url' вакансии.
        db_name (str): Название базы данных.
        db_config (Dict[str, str]): Конфигурация подключения к PostgreSQL, включая название базы данных.

    Returns:
        None
    """
    conn = psycopg2.connect(dbname=db_name, **db_config)
    cur = conn.cursor()

    try:
        for vac in vacancies:
            cur.execute(
                sql.SQL(
                    "INSERT INTO vacancies (vacancy_id, employer_id, name, description, salary, url) "
                    "VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (vacancy_id) DO NOTHING;"),
                (vac['vacancy_id'], vac['employer_id'], vac['name'], vac.get('description'), vac.get('salary'),
                 vac['url'])
            )
        conn.commit()
        print("Данные о вакансиях успешно заполнены")
    except Exception as e:
        print(f"Ошибка при заполнении данных о вакансиях: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
