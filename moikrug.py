import feedparser

feed_url = 'https://moikrug.ru/vacancies/rss?page='

def load_moikrug_rss(url=feed_url):
    i = 0
    vlist = []
    while True:
        d = feedparser.parse(url + str(i))
        if len(d.entries) == 0:
            break
        print('Loading next ' + str(len(d.entries)) + ' vacancies')
        v = {}
        for ent in d.entries:
            try:
                v['city'] = ent['title'].split(' (')[1].split(',')[0].split(')')[0]
                if v['city'] != 'Санкт-Петербург':
                    continue
            except IndexError as identifier:
                continue
            try:
                salar = ent['title'].split('«')[1].split('»')[1]
                if len(salar.split(', от ')) > 1:
                    v['from'] = int(salar.split(', от ')[1].split(' ')[0])*1000
                else:
                    v['from'] = ''
                if len(salar.split(' до ')) > 1:
                    v['to'] = int(salar.split(' до ')[1].split(' ')[0])*1000
                else:
                    v['to'] = ''
            except IndexError as identifier:
                print(ent)
            v['name'] = ent['title'].split('«')[1].split('»')[0]
            v['description'] = ent['description']
            v['employer_name'] = ent['author']
            v['url'] = ent['link']
            v['id'] = ent['guid']
            vlist.append(v)
        i = i + 1
    return vlist

load_moikrug_rss()