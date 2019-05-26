FROM python:3

ADD run.py /

CMD [ "python", "-u", "./run.py" ]