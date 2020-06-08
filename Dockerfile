FROM python:slim-buster

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt


COPY manage.py gunicorn.conf.py /app/
COPY maintenance/ /app/maintenance/
COPY static/ /app/static/
COPY templates/ /app/templates/

RUN pip install -r requirements.txt

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN sudo apt-get update
RUN sudo ACCEPT_EULA=Y apt-get install msodbcsql17
RUN sudo apt-get install libgssapi-krb5-2

EXPOSE 8080

CMD ["gunicorn", "maintenance.wsgi"]
