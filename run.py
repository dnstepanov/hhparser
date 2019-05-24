import json
import urllib3
import certifi
import csv
from currency_converter import CurrencyConverter
from progress.bar import Bar
import time
import gspread
# Service client credential from oauth2client
from oauth2client.service_account import ServiceAccountCredentials

# Определение параметров подключения по http
# (User-Agent, включить проверку сертификатов)
user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) ..'}
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                           ca_certs=certifi.where(),
                           headers=user_agent)

# Запросить первый (i=0) лист данных от HH
wordlist = ['\"computer+vision\"', '\"техническое+зрение\"',
            '\"компьютерное+зрение\"', 'алгоритм', '\"Deep+learning\"',
            '\"нейронная+сеть\"', '\"машинное+обучение\"',
            '\"Data+scientist\"', 'Researcher', 'Keras', 'Tensorflow',
            'Matlab', 'OpenCV', 'ROS', '\"Machine+Learn\"', 'Gazebo',
            'PyTorch', '\"научный+сотрудник\"', 'алгоритмист', 'НИОКР']

notlist = ['SEO', 'преподаватель', 'музей', 'риэлтор', 'продажа',
           '\"русская+литература\"', 'война', 'SMM', '\"Call-центр\"',
           'bitrix', '\"техническая+поддержка\"', 'филологическое',
           '\"Менеджер+по+маркетингу\"', 'экономист', 'юрист', 'цена',
           'повар', 'бухгалтер']

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
url = baseurl + ")&only_with_salary=true&per_page=100&page="

response = http.request('GET', url+str(0))
# Разобрать JSON
data = json.loads(response.data.decode('utf-8'))
items = data['items']

# Определить количество доступных листов
pages = data['pages']
print("Found " + str(data['found']) + " vacancies")
# Запросить все оставшиеся листы из доступных (1..pages-1)
print("Запрос оставшихся листов")
# Собрать все ответы в одном списке items
for i in range(1, pages):
    response = http.request('GET', url+str(i))
    data = json.loads(response.data.decode('utf-8'))
    items.extend(data['items'])

# Преобразователь валют
c = CurrencyConverter()

print("Запрос расширенных данных и фильтрация")
# Фильтровать необходимые данные
filtered_items = []
select_list = ['id', 'name', 'alternate_url']
bar = Bar('Processing', max=len(items), suffix='%(percent).1f%% - %(eta)ds')
for k, item in enumerate(items):
    temp = list(set(select_list).intersection(item))
    res = [item[i] for i in temp]

    # Получение подробной информации о каждой вакансии
    response = http.request('GET', 'https://api.hh.ru/vacancies/'+item['id'])
    data = json.loads(response.data.decode('utf-8'))

    t1 = data['salary']['from']
    t2 = data['salary']['to']
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

    # Коррекция зарплаты, указанной как "на руки" в "до вычета налогов"
    gross = data['salary']['gross']
    if not gross:
        if t1 is not None:
            t1 = t1/0.87
        if t2 is not None:
            t2 = t2/0.87

    # Округление зарплат до целых тысяч
    if t1 is not None:
        t1 = round(round(t1, -3))
    if t2 is not None:
        t2 = round(round(t2, -3))

    # Добавление информации в словарь
    temp.extend(['from', 'to', 'employer_name', 'schedule',
                 'employment', 'experience'])
                #  'key_skills'])
    res.extend([t1, t2, data['employer']['name'], data['schedule']['name'],
                data['employment']['name'], data['experience']['name']])
                # data['key_skills']])
    filtered_items.append(dict(zip(temp, res)))
    bar.next()

bar.finish()

# Фильтрация данных по значениям
banned_employers = ['Homework', 'Рай Авто СПБ', 'U24', 'АО ЗАСЛОН',
                    'РГПУ им. А.И. Герцена', 'ТехноНеруд', 'PSI Co Ltd.',
                    'JCat.ru', 'FBS Inc.', 'РИВ ГОШ, Сеть магазинов']
banned_jobs = ['Менеджер по', 'Автор', 'Курьер', 'Мебель', 'труда',
               'медицин', 'юрист', 'кассир', 'ценообразования', 'персонала',
               'Финансовый аналитик', 'работник', 'Печатник', 'Электроник',
               'диспетчер', 'Инженер по автоматизации', 'клиентского сервиса']


def banned_item(item):
    for bname in banned_employers:
        if bname.lower() in item['employer_name'].lower():
            return False
    for bjob in banned_jobs:
        if bjob.lower() in item['name'].lower():
            return False
    return True


filtered_items2 = filter(banned_item, filtered_items)
filtered_items2 = list(filtered_items2)


def save_to_csv(filename, listname):
    with open(filename, 'w', newline='', encoding='utf-8') as employ_data:
        csvwriter = csv.writer(employ_data, dialect='excel', delimiter=';')
        count = 0
        for vac in listname:
            if count == 0:
                header = vac.keys()
                csvwriter.writerow(header)
                count += 1
            csvwriter.writerow(vac.values())


print("Экспорт в csv")
# Экспортировать список в csv
save_to_csv('hhvacdata.csv', filtered_items2)
save_to_csv('hhvacdata_unfilt.csv', filtered_items)


def save_to_google(listname, rp100s=100):
    # Create scope
    scope = ['https://www.googleapis.com/auth/drive']
    # create some credential using that scope and content of startup_funding.json
    creds = ServiceAccountCredentials.from_json_keyfile_name('My First Project-53694cf60e96.json', scope)
    # create gspread authorize using that credential
    client = gspread.authorize(creds)
    # Now will can access our google sheets we call client.open on StartupName
    sheet = client.open('Вакансии HH 3.0').sheet1
    # pp = pprint.PrettyPrinter()
    # # Access all of the record inside that
    # result = sheet.get_all_record()
    # update values

    count = 0
    for vac in listname:
        if count == 0:
            header = []
            header.extend(vac.keys())
            sheet.clear()
            sheet.append_row(header)

        count += 1
        lst = []
        lst.extend(vac.values())
        sheet.append_row(lst)
        if count % rp100s == 0:
            print('Quota exceeded, waiting 150s, sorry')
            time.sleep(150)


print("Экспорт в google")
save_to_google(filtered_items2)
print("Done!")
