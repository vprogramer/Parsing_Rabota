import re
import requests
from bs4 import BeautifulSoup
import openpyxl
import os.path


def companies_with_vacancies():
    page = 0
    all_teams = list()
    work_types = "developer, web, ml, data+science, mashine+learning, big+data, Analyst, Data+Engineer, ETL, BI, " \
                 "backend, back-end, Automation+QA, devops, security, secops"

    for type in work_types:
        while True:
            url_1_and_3_years = "https://rabota.by/search/vacancy?clusters=true&area=1002&ored_clusters=true&experience=between1And3" \
                  "&enable_snippets=true&salary=&text=Python+{0}&from=suggest_post&page={1}".format(type, str(page))

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

        for i in set(all_teams):
            print(i.text)

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

        for i in set(all_teams):
            print(i.text)


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


def create_new_sheet(wb):
    sheetname = input("Type sheet name: \n")
    sheet = wb.create_sheet(sheetname)
    sheet_head = input("Type sheet head by , (Example: Apple, Banana, Tomato\n")
    # Технология	Вакансии	Резюме	чел/место	Перспективность
    sheet.append(sheet_head.split(","))
    return sheetname


def number_of_vacancies(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/93.0.4577.82 Safari/537.36',}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

        num_vac = soup.find("h1", class_="bloko-header-section-3")
        # print(num_vac.text)
        return int(re.search(r"\d+", num_vac.text).group())
    except AttributeError:
        return 0


def number_of_resume(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/93.0.4577.82 Safari/537.36',}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

        num_resume = soup.find("h1", {"class": "bloko-header-1", "data-qa": "bloko-header-1"}).find_next()
        # print(num_resume.text)
        return int(re.search(r"\d+", num_resume.text).group())
    except AttributeError:
        return 0


def main():
    technologies = "Git, Django, DRF, MySQL, PostgreSQL, redis, asyncio, Flask, aiohttp, FastApi, Starlette, Sanic, " \
                   "unit, MongoDB, Celery, Telegram, bs4, beautiful, pydantic, asyncio, " \
                   "concurrent.futures, Falcon, threading, multiprocessing"
    technologies_ml = "OpenCV, ML, Machine Learning, Computer Vision, sklearn, matplotlib, Keras, TensorFlow, " \
                      "PyTorch, numpy, Databricks, Spark, Kafka, Airflow, Apache AirFlow, SciPy, scikit-image, " \
                      "torchvision, Caffe"
    technologies_devops = "Linux, CI/CD, NGINX, Docker, k8s, Nomad, OpenShift, Bash, Ansible, Jenkins, AWS, Git, " \
                          "Azure, Docker+Compose, Grafana, Prometheus, Clickhouse, Kubernetes, Terraform, " \
                          "PowerShell, OSI, TCP/IP, Zabbix, Kafka, Spark, Redis, Cassandra, ClickHouse, " \
                          "ElasticSearch, Kibana, Fluentd, Zipkin, php-fpm, Memcached, RabbitMQ, ELK, Nexus, " \
                          "Sonarqube, Hashicorp+Nomad, Buffers, protobuf, Apache, gitlab, haproxy, grpc, python"

    if os.path.exists('rabota.xlsx'):
        wb = openpyxl.load_workbook('rabota.xlsx')
    else:
        wb = openpyxl.Workbook()
        print(123)
    sheet_catalog = wb.sheetnames
    new_sheet = None

    while True:
        answer = input("Do you want to create new sheet for new data? Type y or n \n")
        if answer == "y":
            new_sheet = create_new_sheet(wb)
        elif answer == "n":
            break
        else:
            continue

    if bool(new_sheet) is True:
        sheet = wb[new_sheet]
    else:
        sheet = wb.active

    print(123)

    for tech in technologies.split(", "):
        # Перебрать в цікле навыкі і страніцы і опыт работы
        url_1_and_3_years = "https://rabota.by/search/vacancy?clusters=true&area=1002&ored_clusters=true&experience=" \
                            "between1And3&enable_snippets=true&salary=&text=Python+{0}&" \
                            "from=suggest_post".format(tech)

        url_no_experience = "https://rabota.by/search/vacancy?area=1002&search_field=name&search_field=company_name" \
                            "&search_field=description&experience=noExperience&clusters=true&ored_clusters=true" \
                            "&enable_snippets=true&text=Python+{0}&from=suggest_post".format(tech)

        url_resume = "https://rabota.by/search/resume?clusters=True&area=1002&currency_code=BYR&ored_clusters=True" \
                     "&order_by=relevance&logic=normal&pos=full_text&exp_period=all_time&experience=noExperience" \
                     "&experience=between1And3&text=Python+{0}".format(tech)

        # print(number_of_vacancies(url_1_and_3_years))
        # print(number_of_vacancies(url_no_experience))
        # print(number_of_vacancies(url_1_and_3_years)+number_of_vacancies(url_no_experience))
        # write_in_table((tech, number_of_vacancies(url_1_and_3_years) + number_of_vacancies(url_no_experience),
        #                 number_of_resume(url_resume)))
        try:
            sheet.append((tech, number_of_vacancies(url_1_and_3_years) + number_of_vacancies(url_no_experience),
                          number_of_resume(url_resume)))
        except:
            wb.save('rabota.xlsx')
    sheet.append((" ", " ", " "))
    wb.save('rabota.xlsx')

    for tech in technologies_devops.split(", "):
        # Перебрать в цікле навыкі і страніцы і опыт работы
        url_1_and_3_years = "https://rabota.by/search/vacancy?clusters=true&area=1002&ored_clusters=true&experience=" \
                            "between1And3&enable_snippets=true&salary=&text=DevOps+{0}&" \
                            "from=suggest_post".format(tech)

        url_no_experience = "https://rabota.by/search/vacancy?area=1002&search_field=name&search_field=company_name" \
                            "&search_field=description&experience=noExperience&clusters=true&ored_clusters=true" \
                            "&enable_snippets=true&text=DevOps+{0}&from=suggest_post".format(tech)

        url_resume = "https://rabota.by/search/resume?clusters=True&area=1002&currency_code=BYR&ored_clusters=True" \
                     "&order_by=relevance&logic=normal&pos=full_text&exp_period=all_time&experience=noExperience" \
                     "&experience=between1And3&text=DevOps+{0}".format(tech)

        # print(number_of_vacancies(url_1_and_3_years))
        # print(number_of_vacancies(url_no_experience))
        # print(number_of_vacancies(url_1_and_3_years)+number_of_vacancies(url_no_experience))
        # write_in_table((tech, number_of_vacancies(url_1_and_3_years) + number_of_vacancies(url_no_experience),
        #                 number_of_resume(url_resume)))
        try:
            sheet.append((tech, number_of_vacancies(url_1_and_3_years) + number_of_vacancies(url_no_experience),
                          number_of_resume(url_resume)))
        except:
            wb.save('rabota.xlsx')
    sheet.append((" ", " ", " "))
    wb.save('rabota.xlsx')

    for tech in technologies_ml.split(", "):
        # Перебрать в цікле навыкі і страніцы і опыт работы
        url_1_and_3_years = "https://rabota.by/search/vacancy?clusters=true&area=1002&ored_clusters=true&experience=" \
                            "between1And3&enable_snippets=true&salary=&text=Python+{0}&" \
                            "from=suggest_post".format(tech)

        url_no_experience = "https://rabota.by/search/vacancy?area=1002&search_field=name&search_field=company_name" \
                            "&search_field=description&experience=noExperience&clusters=true&ored_clusters=true" \
                            "&enable_snippets=true&text=Python+{0}&from=suggest_post".format(tech)

        url_resume = "https://rabota.by/search/resume?clusters=True&area=1002&currency_code=BYR&ored_clusters=True" \
                     "&order_by=relevance&logic=normal&pos=full_text&exp_period=all_time&experience=noExperience" \
                     "&experience=between1And3&text=Python+{0}".format(tech)

        # print(number_of_vacancies(url_1_and_3_years))
        # print(number_of_vacancies(url_no_experience))
        # print(number_of_vacancies(url_1_and_3_years)+number_of_vacancies(url_no_experience))
        # write_in_table((tech, number_of_vacancies(url_1_and_3_years) + number_of_vacancies(url_no_experience),
        #                 number_of_resume(url_resume)))
        try:
            sheet.append((tech, number_of_vacancies(url_1_and_3_years) + number_of_vacancies(url_no_experience),
                          number_of_resume(url_resume)))
        except:
            wb.save('rabota.xlsx')
    sheet.append((" ", " ", " "))
    wb.save('rabota.xlsx')


if __name__ == "__main__":
    main()
