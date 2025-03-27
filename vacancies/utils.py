from typing import Any

import jmespath
import requests

from constant import HH_EMPLOYERS_ID, HH_URL_EMPLOYERS, HH_URL_VACANCIES


def get_employers() -> list[dict[str, Any]]:
    employers_data = []
    for company_id in HH_EMPLOYERS_ID:
        url = f'{HH_URL_EMPLOYERS}/{company_id}'
        response = requests.get(url=url)
        if response.status_code == 200:
            request = """
            {
                employer_id: id,
                employer_name: name,
                url: alternate_url
            }
            """
            data = jmespath.search(request, response.json())
            employers_data.append(data)
    return employers_data


def get_vacancies(company_id: int) -> list[dict[str, Any]]:
    vacancies_data = []
    url = f'{HH_URL_VACANCIES}?employer_id={company_id}&per_page=100&only_with_salary=true'
    response = requests.get(url=url)
    if response.status_code == 200:
        vacancies = response.json().get('items', [])
        for vac in vacancies:
            salary_from = vac.get('salary', {}).get('from')
            salary_to = vac.get('salary', {}).get('to')
            salary = salary_from if salary_from is not None else salary_to

            request = """
            {
                vacancy_id: id,
                employer_id: employer.id,
                name: name,
                description: snippet.requirement || '' && snippet.responsibility || '',
                salary: salary,
                url: alternate_url
            }
            """
            data = jmespath.search(request, vac)
            data['salary'] = salary
            vacancies_data.append(data)
    return vacancies_data


def get_all_vacancies() -> list[dict[str, Any]]:
    vacancies_data = []
    for company_id in HH_EMPLOYERS_ID:
        vacancies = get_vacancies(company_id)
        vacancies_data.extend(vacancies)
    return vacancies_data
