# MEDIA STREAM

A django web application to stream video content using .m3u8 


# Python setup 
```
- sudo add-apt-repository ppa:deadsnakes/ppa
- sudo apt install python3.10
- python3.10 --version
- curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
- python3.10 get-pip.py
- sudo apt-get install python3.10-distutils
- python3.10 -m pip --version
- python3.10 -m pip install virualenv
- python3.10 -m virtualenv venv
- pip --version
```

### 1. System Requirements
```
- Python 3.10
- Postgres Sql 14
- Ubuntu 20.04 WSL 1 on Windows 11
```

### 2. Project Setup 
```
- git clone https://github.com/NishantGhanate/MediaStream.git
- cd MediaStream
- python3.10 -m virtualenv venv
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

# REDIS
CELERY_BROKER_URL = redis://localhost:6379/1

# Rabbit MQ
CELERY_BROKER_URL = amqp://guest:**@127.0.0.1:5672//

# Timezone 
TIME_ZONE = Asia/Kolkata

# Cache
CACHE_LOCATION = redis://localhost:6379/0
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

In order to use celery we need to setup 

- Redis

OR 

- Erlang
- RabbitMQ on windows 

<br>

### Redis Requirements

- Redis on wsl 2
- redisInsight-v2 [https://redis.com/redis-enterprise/redis-insight/#insight-form]


### Install Redis
```
- sudo apt-get install redis
- redis-server start

Open another wsl2 terminal 

- redis-cli 
```

<hr>

### Rabbit MQ
Using Chocolatey (power shell on admin mode):
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
<hr>

###  Run Celery 
```
celery --app media_stream worker -l info --pool=solo

<syntax> 
celery --app <project_name> worker -l info --pool=solo
celery -A <project_name> worker -l INFO
celery -A <project_name> worker -l info -Q celery, high
```

Note : Make to sure to run migration if you have installed celery later

