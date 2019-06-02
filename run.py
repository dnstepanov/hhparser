import json
import urllib3
import certifi
import csv
from currency_converter import CurrencyConverter
from progress.bar import Bar
import gspread
import sched
import time
import os
from shutil import copyfile
# Service client credential from oauth2client
from oauth2client.service_account import ServiceAccountCredentials
# Слова для поиска определены в words.py
from words import wordlist, notlist, banned_employers, banned_jobs, vac_types

# Configuration
DEBUG_RUN = False
if DEBUG_RUN:
    print('ВНИМАНИЕ! ВКЛЮЧЕНА ОТЛАДКА, ЗАГРУЗИТСЯ ОДИН ЛИСТ!')

# Проверка начальной настройки и определение наличия docker
if os.path.isdir('/cfg'):
    in_docker = True
    bad_vac_fname = '/cfg/badvac.tsv'
    # Проверить, что настройка выполнена, и файл помещен в /cfg
    exists = os.path.isfile(bad_vac_fname)
    if not exists:
        copyfile('badvac.tsv', bad_vac_fname)
else:
    in_docker = False
    bad_vac_fname = 'badvac.tsv'

vac_data_fname = 'hhvacdata.tsv'
vac_base_url = 'https://api.hh.ru/vacancies/'
delay = 3600  # once per our
# Преобразователь валют
c = CurrencyConverter()


def get_vac_type(item):
    """ Возвращает тип вакансии в соответствии со словарем вакансий"""
    for vc in vac_types:
        for kw in vc[1]:
            if kw.lower() in item['name'].lower():
                return vc[0]
    return ''


def not_banned_item(item):
    """ Проверяет, что вакансия не исключена по списку запрещенных слов """
    # Фильтрация по работодателям реализована ранее, до запроса
    # for bname in banned_employers:
    #     if bname.lower() in item['employer_name'].lower():
    #         return False
    for bjob in banned_jobs:
        if bjob.lower() in item['name'].lower():
            return False
    return True


def save_vaclist_to_tsv(filename, listname):
    """ Сохранение списка вакансий listname в файл типа tsv """
    with open(filename, 'w', newline='', encoding='utf-8') as employ_data:
        csvwriter = csv.writer(employ_data, dialect='excel', delimiter='\t')
        count = 0
        for vac in listname:
            if count == 0:
                header = vac.keys()
                csvwriter.writerow(header)
                count += 1
            csvwriter.writerow(vac.values())


def save_list_to_file(filename, listname):
    """ Сохраняет списко в файл (одна запись - одна строка) """
    with open(filename, 'w', newline='', encoding='utf-8') as employ_data:
        for item in listname:
            employ_data.write("%s\n" % item)


def load_vaclist_from_tsv(filename):
    """ Загружает список вакансий из tab-separated file """
    with open(filename, 'r', newline='', encoding='utf-8') as employ_data:
        old_items = {}
        csvreader = csv.reader(employ_data, dialect='excel', delimiter='\t')
        count = 0
        for vac in csvreader:
            if count == 0:
                header = vac
                count += 1
            else:
                row = dict(zip(header, vac))
                ID = row['id']
                old_items[ID] = row
        return old_items


def load_badlist_from_tsv(filename):
    """ Загружает список запрещенных слов для вакансий из файла """
    lst = []
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as employ_data:
            csvreader = csv.reader(employ_data, dialect='excel', delimiter='\n')
            for vac in csvreader:
                lst.extend(vac)
    except FileNotFoundError:
        print('Файл плохих вакансий не найден')
    return lst


def save_to_google(filename):
    """ Выгружает список вакансий в google-таблицу с известным ID, полностью затирая таблицу """
    # Create scope
    scope = ['https://www.googleapis.com/auth/drive']
    # create some credential using that scope and content of startup_funding.json
    creds = ServiceAccountCredentials.from_json_keyfile_name('My First Project-53694cf60e96.json', scope)
    # create gspread authorize using that credential
    client = gspread.authorize(creds)
    # Now will can access our google sheets we call client.open on StartupName
    # sheet = client.open('Вакансии HH 3.0').sheet1
    content = open(filename, 'r', newline='', encoding='utf-8').read()
    # Google не поддерживает разделитель ';', но зато всё ок с Tab
    # content = content.replace(";", '\t')
    client.import_csv('1zNsxWevX9FZxz2CJws9Pjd21KlQBy7KYo6HHSWUhHH8', content.encode('utf-8'))


def load_from_google():
    """ Загружает список вакансий из таблицы """
    # Create scope
    scope = ['https://www.googleapis.com/auth/drive']
    # create some credential using that scope and content of startup_funding.json
    creds = ServiceAccountCredentials.from_json_keyfile_name('My First Project-53694cf60e96.json', scope)
    # create gspread authorize using that credential
    client = gspread.authorize(creds)
    # Now will can access our google sheets we call client.open on StartupName
    sheet = client.open('Вакансии HH 3.0').sheet1
    list_of_lists = sheet.get_all_values()

    old_items = {}
    count = 0
    for vac in list_of_lists:
        if count == 0:
            header = vac
            count += 1
        else:
            row = dict(zip(header, vac))
            ID = row['id']
            old_items[ID] = row

    return old_items


def form_hh_url(wordlist, notlist):
    """ формирует правильный url для запроса HH API из списка слов для OR и NOT """
    baseurl = 'https://api.hh.ru/vacancies?area=2&text=('
    for i, wrd in enumerate(wordlist):
        if i > 0:
            baseurl = baseurl + "+OR+"
        baseurl = baseurl + wrd
    baseurl = baseurl + ")+NOT+("
    for i, wrd in enumerate(notlist):
        if i > 0:
            baseurl = baseurl + "+OR+"
        baseurl = baseurl + wrd
    url = baseurl + ")&only_with_salary=false&per_page=100&page="
    return url


def main(sc):
    # Определение параметров подключения по http
    # (User-Agent, включить проверку сертификатов)
    user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) ..'}
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                               ca_certs=certifi.where(),
                               headers=user_agent)

    # Запросить первый (i=0) лист данных от HH
    url = form_hh_url(wordlist, notlist)
    response = http.request('GET', url+str(0))
    # Разобрать врзвращенный JSON
    data = json.loads(response.data.decode('utf-8'))
    # Определить количество доступных листов
    pages = data['pages']
    print("Found " + str(data['found']) + " vacancies")

    items = data['items']
    # Запросить все оставшиеся листы из доступных (1..pages-1)
    print("Запрос оставшихся " + str(pages-1) + " листов вакансий")
    # Собрать все ответы в одном списке items
    # Для отладки ограничимся одним листом данных
    if DEBUG_RUN:
        pages = 0

    for i in range(1, pages):
        response = http.request('GET', url+str(i))
        data = json.loads(response.data.decode('utf-8'))
        items.extend(data['items'])

    print("Запрос расширенных данных, преобразование и фильтрация")
    filtered_items = []
    select_list = ['id']
    # progress bar, так как операция - долгая
    bar = Bar('Processing', max=len(items), suffix='%(percent).1f%% - %(eta)ds')
    for item in items:

        # Быстрая фильтрация по списку работодателей
        if item['employer']['name'] in banned_employers:
            bar.next()
            continue

        # Быстрая фильтрация по ключевым словам в названии вакансии
        if not not_banned_item(item):
            bar.next()
            continue

        temp = list(set(select_list).intersection(item))
        res = [item[i] for i in temp]

        # Получение подробной информации о каждой вакансии
        response = http.request('GET', vac_base_url+item['id'])
        data = json.loads(response.data.decode('utf-8'))

        t1 = 0
        t2 = 0
        if data['salary'] is not None:
            # Обработка зарплат
            t1 = data['salary']['from']
            t2 = data['salary']['to']

            # Преобразование None в числа - сомнительно, поэтому дальше проверки на None оставлены
            if t1 is None:
                t1 = 0
            if t2 is None:
                t2 = t1
            # Преобразовать валюту в рубли
            if data['salary']['currency'] != 'RUR':
                if t1 is not None:
                    t1 = c.convert(t1, data['salary']['currency'], 'RUB')
                if t2 is not None:
                    t2 = c.convert(t2, data['salary']['currency'], 'RUB')

            # Коррекция зарплаты, указанной как "на руки" в "до вычета налогов" (gross)
            ndfl = 0.13
            gross = data['salary']['gross']
            if not gross:
                if t1 is not None:
                    t1 = t1/(1-ndfl)
                if t2 is not None:
                    t2 = t2/(1-ndfl)

            # Округление зарплат до целых тысяч
            if t1 is not None:
                t1 = round(round(t1, -3))
            if t2 is not None:
                t2 = round(round(t2, -3))

        # Преобразование key_skills в строку, разделенную запятыми
        skills = ''
        for cc, skill in enumerate(data['key_skills']):
            if cc != 0:
                skills = skills + ', '
            skills = skills + skill['name']

        # Определение типа вакансии
        vac_type = get_vac_type(item)

        # Добавление информации в словарь
        temp.extend(['name', 'url', 'vac_type', 'from', 'to', 'employer_name',
                     'schedule', 'employment', 'experience', 'key_skills',
                     'bad'])
        res.extend([item['name'], item['alternate_url'], vac_type, t1, t2,
                    data['employer']['name'], data['schedule']['name'],
                    data['employment']['name'], data['experience']['name'],
                    skills, ''])
        filtered_items.append(dict(zip(temp, res)))
        bar.next()

    bar.finish()
    print("После фильтрации по работодателям и словам осталось "
          + str(len(filtered_items)) + " вакансий")

    old_items = {}
    print('Загружаем старые записи')
    old_items = load_from_google()
    print('Загружено '+str(len(old_items))+" старых вакансий")
    # Выполнить очистку старых вакансий по актуальным правилам
    old_items = {k: v for k, v in old_items.items() if v['employer_name'] not in banned_employers}
    old_items = {k: v for k, v in old_items.items() if not_banned_item(v)}
    print("После фильтрации по актуальным правилам осталось " +
          str(len(old_items))+" старых вакансий")

    # Объединить старые и новые вакансии
    for item in filtered_items:
        old_items[item['id']] = item

    print("После объединения получилось " + str(len(old_items)) + " вакансий")

    # Обновить список плохих вакансий (bad = True)
    print('Обновление списка ID плохих вакансий')
    # Загрузка старого списка плохих вакансий
    bad_vac = load_badlist_from_tsv(bad_vac_fname)
    for k, v in old_items.items():
        if v['bad'] == 'TRUE':
            bad_vac.append(k)
    # Удалить дубликаты ID плохих вакансий
    bad_vac = list(dict.fromkeys(bad_vac))
    # Сохранить обновленный список
    save_list_to_file(bad_vac_fname, bad_vac)
    print('В списке плохих вакансий ' + str(len(bad_vac)) + ' вакансий')

    # Фильтрация объединенного перечня по списку ID плохих вакансий
    cnt = len(old_items)
    old_items = {k: v for k, v in old_items.items() if k not in bad_vac}
    print('По ID удалено ' + str(cnt - len(old_items)) + ' плохих вакансий')

    filtered_items = old_items.values()

    print("Экспорт в tsv")
    # Экспортировать список в csv и в google-таблицу
    save_vaclist_to_tsv(vac_data_fname, filtered_items)
    print("Экспорт в google через загрузку нашего tvs!")
    save_to_google(vac_data_fname)

    print("Done!")

    # Reschedule the main function
    print('Reschedule main after '+str(delay)+' seconds')
    s.enter(delay, 1, main, (sc,))


if __name__ == '__main__':
    # main()
    # sched is used to schedule main function every 30 seconds.
    # for that once main function executes in end,
    # we again schedule it to run in 30 seconds
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, main, (s,))
    s.run()
