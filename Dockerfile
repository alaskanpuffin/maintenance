FROM python:slim-buster

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update
RUN apt-get install -y g++ unixodbc-dev curl ca-certificates gnupg2 wget

RUN pip install -r requirements.txt


COPY manage.py gunicorn.conf.py /app/
COPY maintenance/ /app/maintenance/
COPY static/ /app/static/
COPY templates/ /app/templates/

RUN pip install -r requirements.txt

RUN wget --quiet --output-document - https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN wget --quiet --output-document - https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update
RUN ACCEPT_EULA=Y apt-get -y install msodbcsql17

EXPOSE 8080

CMD ["gunicorn", "maintenance.wsgi"]
