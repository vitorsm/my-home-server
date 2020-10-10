
FROM python:3.7

COPY . .
WORKDIR ./
RUN pip install -r requirements.txt

CMD ["uwsgi", "--http", ":80", "--wsgi-file", "my_home_server/main.py", "--callable", "app", "--buffer-size", "32768"]
