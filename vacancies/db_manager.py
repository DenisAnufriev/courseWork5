import psycopg2
from typing import Dict, Optional, List, Tuple
from config import get_db_config

class DBManager:
    """
    Класс для управления подключением к базе данных и выполнения запросов.
    """

    def __init__(self, db_name, config: Dict[str, str]) -> None:
        """
        Инициализирует экземпляр DBManager.
        Args:
            config (Dict[str, str]): Конфигурация для подключения к базе данных.
        """
        self.config = config
        self.config["dbname"] = db_name

    def __enter__(self) -> 'DBManager':
        """
        Устанавливает соединение с базой данных и возвращает экземпляр DBManager.
        Returns:
            DBManager: Экземпляр DBManager с установленным соединением.
        """
        self.conn = psycopg2.connect(**self.config)
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[Exception]) -> None:
        """
        Закрывает соединение с базой данных и курсор.
        Args:
            exc_type (Optional[type]): Тип исключения, если оно произошло.
            exc_val (Optional[Exception]): Значение исключения, если оно произошло.
            exc_tb (Optional[Exception]): Трассировка стека исключения, если оно произошло.
        """
        if exc_type is not None:
            print(f'Произошла ошибка {exc_type} {exc_val}')
        self.cur.close()
        self.conn.close()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Возвращает список компаний и количество вакансий в каждой из них.
        Returns:
            List[Tuple[str, int]]: Список кортежей, где каждый кортеж содержит название компании и количество вакансий.
        """
        request = """
        SELECT e.employer_name, COUNT(v.vacancy_id) as vacancies_count
        FROM employers e
        LEFT JOIN vacancies v ON e.employer_id = v.employer_id
        GROUP BY e.employer_name
        ORDER BY vacancies_count DESC;
        """
        try:
            self.cur.execute(request)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print(f"Ошибка при поиске компаний и подсчете вакансий: {e}")
            raise
        finally:
            self.conn.close()

    def get_all_vacancies(self) -> List[Tuple[str, str, Optional[int], str]]:
        """
        Возвращает список всех вакансий с информацией о компании, названии вакансии, зарплате и ссылке на вакансию.
        Returns:
            List[Tuple[str, str, Optional[int], str]]: Список кортежей, где каждый кортеж содержит название компании,
            название вакансии, зарплату и ссылку на вакансию.
        """
        request = """
        SELECT e.employer_name, v.name, v.salary, v.url
        FROM employers e
        LEFT JOIN vacancies v ON e.employer_id = v.employer_id
        ORDER BY v.salary DESC;
        """
        try:
            self.cur.execute(request)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print(f"Ошибка при получении вакансий: {e}")
            raise
        finally:
            self.conn.close()

    def get_avg_salary(self) -> Optional[float]:
        """
        Возвращает среднюю зарплату по всем вакансиям.
        Returns:
            Optional[float]: Средняя зарплата по вакансиям или None, если данных нет.
        """
        request = """
        SELECT ROUND(AVG(v.salary)) as avg_salary
        FROM vacancies v
        """
        try:
            self.cur.execute(request)
            result = self.cur.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Ошибка при получении средней зарплаты: {e}")
            raise
        finally:
            self.conn.close()

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, Optional[int], str]]:
        """
        Возвращает список вакансий с зарплатой выше средней по всем вакансиям.
        Returns:
            List[Tuple[str, str, Optional[int], str]]: Список кортежей, где каждый кортеж содержит название компании,
            название вакансии, зарплату и ссылку на вакансию.
        """
        request = """
        WITH avg_salary AS (
            SELECT AVG(salary) AS average_salary
            FROM vacancies
        )
        SELECT e.employer_name, v.name, v.salary, v.url
        FROM vacancies v
        JOIN employers e ON v.employer_id = e.employer_id
        CROSS JOIN avg_salary
        WHERE v.salary > avg_salary.average_salary;
        """
        try:
            self.cur.execute(request)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print(f"Ошибка при получении вакансий с зарплатой выше средней: {e}")
            raise
        finally:
            self.conn.close()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, Optional[int], str]]:
        """
        Возвращает список вакансий, в которых встречается заданное ключевое слово в названии или описании.
        Args:
            keyword (str): Ключевое слово для поиска.
        Returns:
            List[Tuple[str, Optional[int], str]]: Список кортежей, где каждый кортеж содержит название вакансии,
            зарплату и ссылку на вакансию.
        """
        request = """
        SELECT name, salary, url
        FROM vacancies
        WHERE name ILIKE %s OR description ILIKE %s
        """
        params = (f'%{keyword}%', f'%{keyword}%')

        try:
            self.cur.execute(request, params)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print(f"Ошибка при получении вакансий с ключевым словом '{keyword}': {e}")
            raise
        finally:
            self.conn.close()