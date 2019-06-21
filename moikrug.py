import feedparser
from currency_converter import CurrencyConverter
c = CurrencyConverter()  # Преобразователь валют

feed_url = 'https://moikrug.ru/vacancies/rss?page='


def load_moikrug_rss(url=feed_url):
    i = 0
    vlist = {}
    while True:
        d = feedparser.parse(url + str(i))
        i = i + 1
        if len(d.entries) == 0:
            break
        print('Loading next ' + str(len(d.entries)) + ' vacancies')
        for ent in d.entries:
            v = {'id': ent['guid'].split('/')[-1], 'name': ent['title'].split('«')[1].split('»')[0],
                 'url': ent['link'], 'vac_type': '', 'from': '', 'to': '',
                 'employer_name': ent['author'],
                 'schedule': '', 'employment': '', 'experience': '', 'key_skills': '',
                 'bad': '', 'actual': 'True'}
            try:
                city = ent['title'].split(' (')[1].split(',')[0].split(')')[0]
                if city != 'Санкт-Петербург':
                    continue
            except IndexError:
                continue
            try:
                salar = ent['title'].split('«')[1].split('»')[1]
                v['from'] = int(salar.split(', от ')[1].split(' ')[0])*1000
                cur = salar.split('00 ')[-1][:-2]
                if cur.upper() != 'РУБ':
                    v['from'] = c.convert(v['from'], cur.upper(), 'RUB')

            except IndexError:
                v['from'] = ''
            try:
                salar = ent['title'].split('«')[1].split('»')[1]
                v['to'] = int(salar.split(' до ')[1].split(' ')[0])*1000
                cur = salar.split('00 ')[-1][:-2]
                if cur.upper() != 'РУБ':
                    v['to'] = c.convert(v['to'], cur.upper(), 'RUB')
            except IndexError:
                v['to'] = ''
            try:
                v['key_skills'] = ent['description'].split('навыки: ')[1][:-1]
            except IndexError:
                v['key_skills'] = ''

            # Округление зарплат до целых тысяч
            if v['from'] != '':
                v['from'] = round(round(v['from']/0.87, -3))
            if v['to'] != '':
                v['to'] = round(round(v['to']/0.87, -3))

            if ent['description'].find('Полный рабочий день') != -1:
                v['employment'] = 'Полная занятость'
                v['schedule'] = 'Полный день'
            if ent['description'].find('Неполный рабочий день') != -1:
                v['employment'] = 'Частичная занятость'
            if ent['title'].find('Senior') != -1:
                v['experience'] = 'От 3 до 6 лет'
            if ent['title'].find('Junior') != -1:
                v['experience'] = 'Нет опыта'
            if ent['title'].find('Lead ') != -1:
                v['experience'] = 'От 3 до 6 лет'
            if ent['title'].find('Middle ') != -1:
                v['experience'] = 'От 1 года до 3 лет'
            if v['experience'] == '':
                v['experience'] = 'От 1 года до 3 лет'
            vlist[v['id']] = v
    return vlist


if __name__ == '__main__':
    load_moikrug_rss()