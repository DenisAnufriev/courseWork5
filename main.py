from vacancies.user_menu import user_menu
from vacancies.utils import get_employers, get_all_vacancies
from vacancies.db_create import create_database, create_tables, insert_employers, insert_vacancies
from config import get_db_config

def main() -> None:
    """
    Инициализирует базу данных, создавая базу, таблицы и заполняя их данными о работодателях и вакансиях.
    """
    config = get_db_config()
    db_name = 'HeadHunter'
    print('Создание базы данных ...\n')
    create_database(db_name, config)
    create_tables(db_name, config)

    print('Получение данных о работодателях и вакансиях ...\n')
    employers_data = get_employers()
    vacancies_data = get_all_vacancies()


    insert_employers(employers_data, db_name, config)
    insert_vacancies(vacancies_data, db_name, config)
    print("База данных успешно инициализирована\n")
    user_menu()


if __name__ == '__main__':
    main()

