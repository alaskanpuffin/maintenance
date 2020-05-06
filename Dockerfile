FROM python:latest

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY manage.py gunicorn.conf.py /app/
COPY maintenance/ /app/maintenance/
COPY static/ /app/static/
COPY templates/ /app/templates/

EXPOSE 8080

CMD ["gunicorn", "maintenance.wsgi"]
