# MEDIA STREAM

A django web application to stream video content using .m3u8 


### 1. Requirements
```
- Python 3.10
- Postgres Sql 14
- Windows 11
- WSL 2
```

### 2. Setup 
```
- git clone https://github.com/NishantGhanate/MediaStream.git

- cd MediaStream

- pip install virutalenv

- python -m virtualenv venv

- venv.bat or venv\Scripts\activate

- pip install -r requirements.txt 
```

### 3. Generate Django secret key :
```python
from django.core.management.utils import get_random_secret_key

get_random_secret_key()

'[SECRET KEY]'
```

### 4. Create .env file in project root
```python

# Settings
SECRET_KEY = django-insecure-...........
DEBUG = True
ALLOWED_HOSTS = 127.0.0.1, localhost

# Database
DB_NAME = media_stream
DB_USER = postgres
DB_PASSWORD = my_pwd
DB_HOST = localhost
DB_PORT = 5432

# Timezone 
TIME_ZONE = Asia/Kolkata
```

### 5. Run server
```
- python manage.py makemigrations

- python manage.py migrate

- python manage.py createsuperuser

- python manage.py runserver 0.0.0.0:8000
```

<hr>

## Celery Setup 

In order to use celery we need to setup two things first
- Erlang
- RabbitMQ on windows 


### Rabbit MQ
Using Chocolatey (ps on admin mode):
> choco install rabbitmq

OR 

Install mannually 


### 1. Erlang : https://www.erlang.org/downloads
```
- First install erlang & add to path 

1 - Search edit environment variables for your account, 
    go to advanced > Enviroment varibales

2- Set environment variable:
    Variable name : ERLANG_HOME
    Variable value: C:\Program Files\Erlang

Note: Don't include bin on above step.

3- Append to the PATH environmental variable:
    Variable name : PATH
    Variable value: %ERLANG_HOME%\bin
```

### 2. RabbitMQ : https://www.rabbitmq.com/install-windows.html
```
> D:\Program Files\RabbitMQ Server\rabbitmq_server-3.10.5\sbin>
> rabbitmqctl.bat status
> rabbitmq-service.bat start | stop
```
Open : http://localhost:15672/mgmt
```yml
Username: guest
Password: guest
```

### 3. Run Celery 
```
celery --app <project_name> worker -l info --pool=solo
celery -A <project_name> worker -l INFO
celery -A <project_name> worker -l info -Q celery, high

celery --app media_stream worker -l info --pool=solo
```

Note : Make to sure to run migration if you have installed celery later

## Redis Setup

Requirements 
- Redis on wsl 2
- redisInsight-v2
