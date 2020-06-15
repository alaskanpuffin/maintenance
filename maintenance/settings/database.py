import os

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATABASE_ENGINE = os.environ['DB_ENGINE']

if DATABASE_ENGINE == "sqlite":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR , 'db.sqlite3'),
        }
    }
elif DATABASE_ENGINE == "mssql":
    DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USERNAME'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': '',

        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },

    }

