Скрипт для парсинга вакансий с HeadHunter и "Мой круг", выгрузки данных в таблицу Google и расчёта статистики по профессиям.
Для работы с Google API необходимо получить .json-файл с ключами OAuth2:
https://gspread.readthedocs.io/en/latest/oauth2.html

По умолчанию файл ищется как gapi_auth.json в папке проекта и в папке /cfg (для использования в Docker-контейнере)

При запуске контейнера Docker необходимо задавать расположение папки данных /cfg, например, так:
docker run -v c:/temp:/cfg -it dnstepanov/hhparser

Репозиторий с актуальным докер-контейнером:
https://hub.docker.com/r/dnstepanov/hhparser
