
FROM python:3.7

COPY . .
WORKDIR ./
RUN pip install -r requirements.txt

CMD ["uwsgi", "--http", ":80", "-w", "my_home_server.wsgi:app", "--buffer-size", "32768"]
