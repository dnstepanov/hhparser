# Ключевые слова для запроса
wordlist = ['\"computer+vision\"', '\"техническое+зрение\"',
            '\"компьютерное+зрение\"', 'алгоритм', '\"Deep+learning\"',
            '\"нейронная+сеть\"', '\"машинное+обучение\"', 'разработчик',
            '\"Data+scientist\"', 'Researcher', 'Keras', 'Tensorflow',
            'Matlab', 'OpenCV', 'ROS', '\"Machine+Learn\"', 'Gazebo',
            'PyTorch', '\"научный+сотрудник\"', 'алгоритмист', 'НИОКР',
            '\"Разработка+ПО\"', '\"Проектирование+программного+обеспечения\"',
            '\"Руководитель+IT+проектов\"', '\"система+управления\"',
            'безэкипажный', 'распознавание', '\"team+lead\"', 'C++',
            'Python', 'XGBoost', 'git', 'QT', '\"Visual+Studio\"', 'redmine',
            'SLAM', 'PCL', 'Octave', 'Kalman', 'Калман', '\"Sensor+Fusion\"',
            '\"reinforcement+learning\"', 'беспилотный', '\"начальник+лаборатории\"',
            '\"Начальник+отдела\"', 'программист', 'инженер', 'engineer']

# Ключевые слова для исключения (NOT)
notlist = ['SEO', 'преподаватель', 'риэлтор', 'продажа',
           '\"русская+литература\"', 'SMM', '\"Call-центр\"',
           'bitrix',
           '\"Менеджер+по+маркетингу\"', 'цена',
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
               'медицин', 'юрист', 'кассир', 'ценообразования', 'персонал',
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
               'кулинар', 'персонал', 'управляющий',
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
               'возврат', 'клинич', 'закуп',
               'начальник производства', 'маникюр', 'магазин',
               'recruiter', 'Cyprus', 'аниматор',
               'Сочи', 'литограф', 'судостро', 'официант', 'рецепц',
               'музе', 'Специалист по КДП', 'партнер', 'partner',
               'linguist', 'Кипр', 'копирайт', 'buyer',
               'Finland', 'Autobahn', 'страхов',
               'общего отдела', 'отдела управления НСИ',
               'внедрение ERP', 'тарифообраз', 'мобильн', 'электротех',
               'здани', 'международ', 'профори', 'сварочно', 'материально',
               'мерченд', 'снабже', 'инженер-технолог', 'ремонт',
               'Инженер по подготовке производства', 'Заведующий хозяйством',
               'отдела охраны', 'ВЭД', 'poland', 'bulgaria',
               'организационного отдела', 'отдел нормативно-справочной',
               'HR ']

# Типы опыта
exp_types = ['Нет опыта', 'От 1 года до 3 лет', 'От 3 до 6 лет', 'Более 6 лет']
# Типы вакансий
vac_types = [('Тестировщик', ['Тестиров', 'QA', 'качества', 'test', 'quality', 'тестового']),
             ('Стажер', ['стажер', 'стажёр', 'Cтажер', 'intern']),
             ('СТЗ', ['зрени', 'vision', 'opencv', 'видео', 'изображен']),
             ('Научный сотрудник', ['научный', 'исследоват', 'research', 'алгоритм', 'математ', 'численн', 'R & D', 'R&D', 'Scientist', 'Quantitative','Специалист по цифровой', 'Autonomous Driving Control Systems Engineer']),
             ('Data scientist', ['data sci', 'machine learn', 'big data', 'data engineer', 'нейрон', 'машинно', 'Data Analyst', 'deep']),
             ('Team lead', ['lead', 'scrum', 'project manager', 'product manager', 'менеджер проект', 'менеджер it-проект', 'chief', 'Product owner']),
             ('Python', ['Python']),
             ('Базы данных', ['Баз данных', 'SQL', 'database admin', 'Oracle']),
             ('DevOps/DBA', ['Configuration Manager', 'Release Engineer', 'NOC Engineer', 'Devops', 'девопс', 'Build engineer', 'Системный инженер', 'поддержке Unix', 'administrator', 'it engineer', 'Continuous Integration', 'DBA', 'reliability']),
             ('C#', ['.Net', 'C#', 'С# Developer', 'программист С#', 'С#']),
             ('C/C++', ['++', 'Разработчик C', 'Программист C', 'QT', 'драйвер', 'embed', 'firmware']),
             ('Безопасность', ['безопасн', 'пентест', 'malware', 'защищ', 'security', 'penetrat']),
             ('PHP', ['PHP']),
             ('Delphi', ['Delphi']),
             ('Ruby', ['Ruby']),
             ('FPGA', ['FPGA', 'ПЛИС']),
             ('Erlang', ['Erlang']),
             ('SCALA', ['Scala']),
             ('Архитектор IT', ['архитект']),
             ('Дизайнер', ['UX ', 'UI ', 'UX/UI', 'UX-', 'UI-', 'дизайн']),
             ('Full stack', ['Full', 'фулл', 'web', 'веб']),
             ('Frontend', ['React', 'фронт', 'front', 'Angular', 'Magento', 'Web-разработчик', 'интерфейс']),
             ('Backend', ['Backend', 'back-end']),
             ('Android', ['Android']),
             ('Business Analyst', ['Business analyst']),
             ('Игры', ['game', 'unity', 'игр']),
             ('iOS', ['iOS', 'Swift', 'Objective-C']),
             ('JavaScript', ['JavaScript', 'Node.js', 'nodejs']),
             ('Java', ['Java', 'Spring', 'Kotlin']),
             ('golang', ['golang', 'программист go', 'Go Developer']),
             ('Документация', ['документац', 'защите инф', 'писатель', 'Technical Writer']),
             ('Техподдержка', ['Customer support', 'поддержк', 'support engineer', 'сопровожден', 'service desk', 'helpdesk'),
             ('АСУТП', ['АСУП', 'АСУ ТП', 'MES']),
             ('Начальник', ['Начальник отдела', 'Начальник лаборатории', 'CTO', 'Начальник службы', 'начальника отдела', 'руководител', 'Начальник технологического бюро', 'заведующий лабораторией', 'начальник сектора', 'head', 'директор']),
             ('Инженер', ['Инженер']),
             ('ABAP/SAP', ['ABAP', 'SAP']),
             ('Сисадмин', ['Специалист по IT', 'it-специалист', 'системный администратор']),
             ('Программист прочий', ['Программист', 'Software Principal Engineer', 'Software engineer', 'Developer', 'Разработчик приложений', 'SCALA', 'programmer', 'разработчик'])]
