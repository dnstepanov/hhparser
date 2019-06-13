# Ключевые слова для запроса
wordlist = ['\"computer+vision\"', '\"техническое+зрение\"',
            '\"компьютерное+зрение\"', 'алгоритм', '\"Deep+learning\"',
            '\"нейронная+сеть\"', '\"машинное+обучение\"',
            '\"Data+scientist\"', 'Researcher', 'Keras', 'Tensorflow',
            'Matlab', 'OpenCV', 'ROS', '\"Machine+Learn\"', 'Gazebo',
            'PyTorch', '\"научный+сотрудник\"', 'алгоритмист', 'НИОКР',
            '\"Разработка+ПО\"', '\"Проектирование+программного+обеспечения\"',
            '\"Руководитель+IT+проектов\"', '\"система+управления\"',
            'безэкипажный', 'распознавание', '\"team+lead\"', 'C++',
            'Python', 'XGBoost', 'git', 'QT', '\"Visual+Studio\"', 'redmine',
            'SLAM', 'PCL', 'Octave', 'Kalman', 'Калман', '\"Sensor+Fusion\"',
            '\"reinforcement+learning\"', 'беспилотный', '\"начальник+лаборатории\"',
            '\"Начальник+отдела\"']

# Ключевые слова для исключения (NOT)
notlist = ['SEO', 'преподаватель', 'риэлтор', 'продажа',
           '\"русская+литература\"', 'SMM', '\"Call-центр\"',
           'bitrix', '\"техническая+поддержка\"',
           '\"Менеджер+по+маркетингу\"', 'цена', '\"системный+администратор\"',
           'solidworks', 'p-cad', 'AutoCad', 'конструктор', 'Blender']

# Фильтрация данных по значениям
# Исключаемые работодатели (точное написание!!!)
banned_employers = ['Homework', 'Рай Авто СПБ', 'U24', 'АО ЗАСЛОН',
                    'РГПУ им. А.И. Герцена', 'ТехноНеруд', 'PSI Co Ltd.',
                    'JCat.ru', 'FBS Inc.', 'РИВ ГОШ, Сеть магазинов',
                    '2Nova Interactive', 'УК Грандо', 'Стройметиз',
                    'ИСМИРА', 'ЦЕНТРАЛЬНОЕ ЖИЛИЩНО-КОММУНАЛЬНОЕ УПРАВЛЕНИЕ',
                    'Космосервис Управление', 'СофтБаланс', 'Инстамарт',
                    'Мясоперерабатывающий завод Иней', 'Работут', 'Skyeng',
                    'Российские Кадастровые Системы', 'ПКБ', 'Гурмания',
                    'Фотостудия сюжетная линия', 'Space307', 'ЦЕНТРОФИНАНС',
                    'ПНК имени Кирова', 'Прагматика', 'Градиент', 'Николь',
                    'ANY Group', 'Sun Sea Escapes', 'Неовижн', 'ВЕБИМ.РУ',
                    'Столичный кейтеринг', 'МРСК Северо-Запада', 'Мой Зубной',
                    'АНО Агентство по Развитию Человеческого Капитала На Дальнем Востоке',
                    'Fmedia', 'REVO Capital LLC', 'Crossover', 'ДИДЖИТАЛ ТРЕЙД СОЛЮШНС',
                    'EOtradex', 'Clean City', 'ОКЕЙ – Федеральная розничная сеть',
                    'АК-Сервис', 'Суши-бар КИ-DO', 'УК ФЦ Николаевский',
                    'Васильева Елизавета Александровна', 'Nesco', 'Перекресток',
                    'Администрация Городского Округа Кашира', 'Пятерочка',
                    'Газпром теплоэнерго', 'Красное & Белое, розничная сеть',
                    'Вентиляционные системы', 'Ленэнерго', 'ЛКХП Кирова',
                    'Переводческая компания ТРАНСТЕХ', 'Эльтон-C', 'Рекрутинговый центр Персонал']

# Исключаемые фразы из названия вакансий (подстрока, любой регистр)
banned_jobs = ['Менеджер по', 'Автор', 'Курьер', 'Мебель', 'труда',
               'медицин', 'юрист', 'кассир', 'ценообразования', 'персонала',
               'Финансовый аналитик', 'работник', 'Печатник', 'Электроник',
               'диспетчер', 'клиентского сервиса',
               'филологическое', 'экономист', 'юрист', 'повар', 'бухгалтер',
               'войн', 'электрик', 'механик', 'ночной', 'сервис', 'частей',
               'разнорабочий', 'прачечн', 'химик', 'Товаровед', 'Паяльщик',
               'прораб', 'водитель', 'кладовщик', 'горничная', 'оператор',
               'кадров', 'координатор', 'финансовый', 'аудитор', 'Портной',
               'бариста', '-менеджер', '1C', '1С', 'помощник', 'Отделочник',
               'Бетонщик', 'ассистент', 'рекрутер', 'Financial Manager',
               'логист', 'секретарь', 'нормоконтрол', 'экономического',
               'слаботочных', 'тренер', 'продавец', 'слесарь', 'монтаж',
               'сиделка', 'задолженно', 'флорист', 'продавец', 'мерчендайзер',
               'перевод', 'маляр', 'мастер по', 'кондитер', 'грузчик',
               'кулинар', 'персонал', 'администратор', 'управляющий',
               'трубопровод', 'биолог', 'планированию', 'Администратор отдела',
               'документооборот', 'Уборщи', 'Главный инженер', 'Охранник',
               'телефон', '1 С', 'ревизор', 'обучен', 'комплектац',
               'HR менеджер', 'контактного', 'интерьер', 'верстальщик',
               'Эксперт по расчёту', 'кадрам', 'по платежам', 'заработной',
               'гостей', 'реклам', 'учебных', 'налог', 'шлифов', 'акушер',
               'сертифик', 'социальны', 'экономи', 'Междисциплинарные',
               'истори', 'торговы', 'главный технолог', 'по сервису',
               'контролер', 'АСКУЭ', 'МСФО', 'тендер', 'продвижени',
               'экспедитор', 'полицей', 'клиент', 'бармен',
               'HR-', 'врач', 'Консультант SAP BPC',
               'переплетчик', 'учет', 'юридич', 'столовая', 'лифт',
               'аналитик', 'Artist', 'юрис', 'слаботоч', 'табель',
               'возврат', 'клинич', 'закуп', 'Unity', 'Front',
               'начальник производства', 'маникюр', 'магазин',
               'recruiter', 'Cyprus', 'аниматор',
               'Сочи', 'литограф', 'судостро',
               'музе', 'Специалист по КДП', 'партнер', 'partner', 'back',
               'linguist', 'Кипр', 'копирайт', 'buyer',
               'Finland', 'Autobahn', 'Oracle', 'страхов', 'инженер АСУ ТП',
               'общего отдела', 'отдела управления НСИ',
               'внедрение ERP', 'тарифообраз', 'мобильн', 'электротех',
               'здани', 'международ', 'профори', 'сварочно', 'материально',
               'мерченд', 'снабже', 'инженер-технолог', 'ремонт',
               'Инженер по подготовке производства', 'Заведующий хозяйством',
               'отдела охраны', 'ВЭД',
               'организационного отдела', 'отдел нормативно-справочной',
               'HR ']

# Типы опыта
exp_types = ['Нет опыта', 'От 1 года до 3 лет', 'От 3 до 6 лет', 'Более 6 лет']
# Типы вакансий
vac_types = [('Тестировщик', ['Тестиров', 'QA', 'качества', 'test', 'quality']),
             ('Стажер', ['стажер', 'стажёр']),
             ('СТЗ', ['зрени', 'vision', 'opencv', 'видео']),
             ('Научный сотрудник', ['научный', 'исследоват', 'research', 'алгоритм', 'математ', 'численн']),
             ('Data scientist', ['data sci', 'machine learn', 'big data', 'data engineer', 'нейрон']),
             ('Team lead', ['team', 'lead', 'scrum', 'project manager', 'product manager', 'менеджер проект', 'менеджер it-проект']),
             ('Python', ['Python']),
             ('Базы данных', ['Баз данных', 'SQL', 'database admin']),
             ('DevOps/DBA', ['Devops', 'девопс', 'Configuration manager/Build engineer', 'Системный инженер', 'поддержке Unix', 'administrator', 'it engineer']),
             ('C/C++', ['++', 'Разработчик C']),
             ('C#', ['.Net', 'C#']),
             ('Java', ['Java']),
             ('PHP', ['PHP']),
             ('Delphi', ['Delphi']),
             ('Ruby', ['Ruby']),
             ('iOS', ['iOS', 'Swift', 'Objective-C']),
             ('FPGA', ['FPGA', 'ПЛИС']),
             ('Android', ['Android']),
             ('Erlang', ['Erlang']),
             ('Архитектор IT', ['архитект']),
             ('Дизайнер', ['UX', 'UI','дизайн']),
             ('Frontend', ['React', 'фронт', 'front', 'Angular', 'Magento', 'Web-разработчик']),
             ('Full stack', ['Full', 'фулл']),
             ('golang', ['golang']),
             ('Документация', ['документац', 'защите инф', 'писатель', 'Technical Writer']),
             ('Техподдержка', ['Customer support', 'поддержк', 'support engineer']),
             ('Начальник', ['Начальник отдела', 'Начальник лаборатории', 'CTO', 'начальника отдела', 'руководителя отдела', 'Начальник технологического бюро', 'заведующий лабораторией', 'начальник сектора', 'head', 'директор']),
             ('Программист', ['Программист', 'Software engineer', 'Developer', 'Разработчик приложений', 'SCALA', 'programmer']),
             ('Инженер', ['Инженер'])]
