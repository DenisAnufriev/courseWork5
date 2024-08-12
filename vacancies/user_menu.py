from vacancies.utils import get_employers, get_all_vacancies
from vacancies.db_create import create_database, create_tables, insert_employers, insert_vacancies
from vacancies.db_manager import DBManager
from config import get_db_config

DB_CONFIG = get_db_config()
DB_NAME = 'HeadHunter'

def user_menu() -> None:
    """
    Основная функция для взаимодействия с пользователем.
    """
    input('Добро пожаловать!\nНажмите Enter для начала работы\n')

    print('Получение вакансий из API hh.ru. Пожалуйста подождите ...\n')
    employers_data = get_employers()
    vacancies_data = get_all_vacancies()
    print(f'Получено {len(vacancies_data)} вакансий от {len(employers_data)} работодателей\n')

    # print('Создание и наполнение базы данных ...\n')
    # create_database(DB_NAME, DB_CONFIG)
    # create_tables(DB_NAME, DB_CONFIG)
    # print('Получение данных о работодателях и вакансиях ...\n')
    # insert_employers(employers_data, DB_NAME, DB_CONFIG)
    # insert_vacancies(vacancies_data, DB_NAME, DB_CONFIG)
    # print("База данных успешно инициализирована\n")
    print()

    while True:
        print('\n1. Получить список всех компаний и количество вакансий у каждой компании')
        print('2. Получить список всех вакансий с указанием компании, вакансии, зарплаты и ссылки на вакансию')
        print('3. Получить среднюю зарплату по вакансиям')
        print('4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям')
        print('5. Получить список всех вакансий, в названии которых содержатся переданные в метод слова')
        print('6. Выход')

        user_input = input('Выберите пункт меню: \n')
        print()

        if user_input == '1':
            menu_get_all_emp_count_vac()
        elif user_input == '2':
            menu_get_all_vac()
        elif user_input == '3':
            menu_get_avg_salary()
        elif user_input == '4':
            menu_get_vac_higher_avg()
        elif user_input == '5':
            menu_get_vac_keyword()
        elif user_input == '6':
            print("\nВыход из программы\n")
            break
        else:
            print('\nНекорректный выбор, попробуйте еще раз\n')


def menu_get_all_emp_count_vac() -> None:
    """
    Функция для взаимодействия с пользователем при выборе
    'Получить список всех компаний и количество вакансий у каждой компании'.
    """

    with DBManager(DB_NAME, DB_CONFIG) as db_manager:
        companies_vacancies = db_manager.get_companies_and_vacancies_count()
        if companies_vacancies:
            for row in companies_vacancies:
                # print(row)
                print(f'Компания: {row[0]}, Количество вакансий: {row[1]}')
        else:
            print("\nНет данных для отображения.")


def menu_get_all_vac() -> None:
    """
    Функция для взаимодействия с пользователем при выборе
    'Получить список всех вакансий с указанием компании, вакансии, зарплаты и ссылки на вакансию'.
    """

    with DBManager(DB_NAME, DB_CONFIG) as db_manager:
        vacancies = db_manager.get_all_vacancies()
        if vacancies:
            for row in vacancies:
                print(f'Компания: {row[0]}, Вакансия: {row[1]}, Зарплата: {row[2]}, Ссылка: {row[3]}')
        else:
            print("\nНет данных для отображения.")


def menu_get_avg_salary() -> None:
    """
    Функция для взаимодействия с пользователем при выборе
    'Получить среднюю зарплату по вакансиям'.
    """

    with DBManager(DB_NAME, DB_CONFIG) as db_manager:
        avg_salary = db_manager.get_avg_salary()
        if avg_salary is not None:
            print(f'Средняя зарплата: {avg_salary}')
        else:
            print("\nНет данных для отображения.")


def menu_get_vac_higher_avg() -> None:
    """
    Функция для взаимодействия с пользователем при выборе
    'Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям'.
    """

    with DBManager(DB_NAME, DB_CONFIG) as db_manager:
        vac_higher = db_manager.get_vacancies_with_higher_salary()
        if vac_higher:
            for row in vac_higher:
                print(f'Компания: {row[0]}, Вакансия: {row[1]}, Зарплата: {row[2]}, Ссылка: {row[3]}')
        else:
            print("\nНет данных для отображения.")


def menu_get_vac_keyword() -> None:
    """
    Функция для взаимодействия с пользователем при выборе
    'Получить список всех вакансий, в названии которых содержатся переданные в метод слова'.
    """
    user_input = input('\nВведите слово для поиска\n')

    with DBManager(DB_NAME, DB_CONFIG) as db_manager:
        vac_keyword = db_manager.get_vacancies_with_keyword(user_input)
        if vac_keyword:
            for row in vac_keyword:
                print(f'Вакансия: {row[0]}, Зарплата: {row[1]}, Ссылка: {row[2]}')
        else:
            print("\nНет данных для отображения.")
