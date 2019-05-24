import json
import redis
import urllib3
import certifi
import csv

# Определение параметров подключения по http (User-Agent, включить проверку сертификатов)
user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) ..'}
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                           ca_certs=certifi.where(),
                           headers=user_agent)

# Запросить первый (i=0) лист данных от HH
i = 0
url = 'https://api.hh.ru/vacancies?area=2&text=(\"computer+vision\"+OR+\"техническое+зрение\"+OR+\"компьютерное+зрение\"+OR+\"алгоритм\"+OR+\"Deep+learning\"+OR+\"нейронная+сеть\"+OR+\"машинное+обучение\"+OR+\"научный+сотрудник\"+OR+алгоритмист+OR+НИОКР)+NOT+(SEO+OR+преподаватель+OR+музей+OR+риэлтор+OR+продажа+OR+\"русская+литература\"+OR+война+OR+SMM+OR+\"Call-центр\"+OR+bitrix+OR+\"техническая+поддержка\"+OR+филологическое+OR+экономист+OR+юрист+OR+цена)&only_with_salary=true&per_page=100&page='
response = http.request('GET', url+str(i))
# Разобрать JSON
data = json.loads(response.data.decode('utf-8'))
items = data['items']

# Определить количетство листов
pages = data['pages']

# Запросить каждый лист из доступных (0..pages-1)
# Собрать все ответы в одной базе данных
for i in range(1, pages):
    response = http.request('GET', url+str(i))
    data = json.loads(response.data.decode('utf-8'))
    items.extend(data['items'])

with open('hhvacdata.csv', 'w', newline='', encoding='utf-8') as employ_data:
    csvwriter = csv.writer(employ_data, dialect='excel', delimiter=';')

    count = 0
    for vac in items:
        if count == 0:
            header = vac.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(vac.values())
