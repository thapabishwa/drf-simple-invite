FROM python:3.6

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY example code

WORKDIR code

EXPOSE 8000

CMD ./manage.py migrate && \
    ./manage.py collectstatic --noinput && \
    newrelic-admin run-program gunicorn --bind 0.0.0.0:8000 --access-logfile - example.wsgi:application

