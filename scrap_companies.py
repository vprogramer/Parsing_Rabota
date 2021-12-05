import re
import requests
from bs4 import BeautifulSoup
import openpyxl
import os.path


def companies_with_vacancies():
    page = 0
    all_teams = list()
    work_types = "developer, web, ml, data+science, maсhine+learning, big+data, Analyst, Data+Engineer, ETL, BI, " \
                 "backend, back-end, Automation+QA, devops, security, secops"
    language = "Python"

    for work in work_types:
        while True:
            url_1_and_3_years = "https://rabota.by/search/vacancy?clusters=true&area=1002&ored_clusters=true&experience=between1And3" \
                  "&enable_snippets=true&salary=&text={0}+{1}&from=suggest_post&page={2}".format(language, work, str(page))

            # url_no_experience = "https://rabota.by/search/vacancy?area=1002&search_field=name&search_field=company_name" \
            #                     "&search_field=description&experience=noExperience&clusters=true&ored_clusters=true" \
            #                     "&enable_snippets=true&text=Python+{0}&from=suggest_post&page={1}".format(type, str(page))


            # url_resume = "https://rabota.by/search/resume?clusters=True&area=1002&currency_code=BYR&ored_clusters=True" \
            #              "&order_by=relevance&logic=normal&pos=full_text&exp_period=all_time&experience=noExperience" \
            #              "&experience=between1And3&text=Python+{0}&page={1}".format(tech, "0")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/93.0.4577.82 Safari/537.36', }
            r = requests.get(url_1_and_3_years, headers=headers)
            soup = BeautifulSoup(r.text, "lxml")
            try:
                soup.find("a", {"class": "bloko-button", "data-qa": "pager-next"}).find("span").text != "дальше"
            except AttributeError:
                break
            page = page + 1
            companies = soup.find_all("a", {"class": "bloko-link bloko-link_secondary",
                                            "data-qa": "vacancy-serp__vacancy-employer"})
            all_teams.extend([com.text for com in companies])

        for i in all_teams:
            for j in work_types:
                print(j, i)



        while True:
            # url_1_and_3_years = "https://rabota.by/search/vacancy?clusters=true&area=1002&ored_clusters=true&experience=between1And3" \
            #       "&enable_snippets=true&salary=&text=Python+{0}&from=suggest_post&page={1}".format(type, str(page))

            url_no_experience = "https://rabota.by/search/vacancy?area=1002&search_field=name&search_field=company_name" \
                                "&search_field=description&experience=noExperience&clusters=true&ored_clusters=true" \
                                "&enable_snippets=true&text=Python+{0}&from=suggest_post&page={1}".format(type, str(page))

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/93.0.4577.82 Safari/537.36', }
            r = requests.get(url_no_experience, headers=headers)
            soup = BeautifulSoup(r.text, "lxml")
            try:
                soup.find("a", {"class": "bloko-button", "data-qa": "pager-next"}).find("span").text != "дальше"
            except AttributeError:
                break
            page = page + 1
            companies = soup.find_all("a", {"class": "bloko-link bloko-link_secondary",
                                            "data-qa": "vacancy-serp__vacancy-employer"})
            all_teams.extend([com.text for com in companies])
            print(all_teams)

        print(2)
        for i in all_teams:
            for j in work_types:
                print(j, i)


def teams_from_resume():
    all_teams = list()
    page = 0
    while True:
        url_python = "https://rabota.by/search/resume?clusters=True&area=1002&currency_code=BYR&ored_clusters=True" \
                     "&order_by=relevance&logic=normal&pos=full_text&exp_period=all_time&text=Python"
        url_devops = "https://rabota.by/search/resume?clusters=True&area=1002&currency_code=BYR&ored_clusters=True" \
                     "&order_by=relevance&logic=normal&pos=full_text&exp_period=all_time&text=devops"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/93.0.4577.82 Safari/537.36', }
        r = requests.get(url_python, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        try:
            soup.find("a", {"class": "bloko-button", "data-qa": "pager-next"}).find("span").text != "дальше"
        except AttributeError:
            break
        page = page + 1
        companies = soup.find_all("span", class_="bloko-text bloko-text_strong")
        all_teams.extend([com.text for com in companies])
        print(all_teams)


if __name__ == "__main__":
    companies_with_vacancies()
