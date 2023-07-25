# MEDIA STREAM

A django web application to stream video content using .m3u8 


### System Requirements used for development
```
- Python 3.9
- Postgres Sql 14
- Ubuntu 20.04 WSL 1 on Windows 11
```



### 2. Project Setup 
```
- git clone https://github.com/NishantGhanate/MediaStream.git
- cd MediaStream
```

### 3. Generate secret key :
```python
If you already have django on your system

C:\Users\nishant>python
>> from django.core.management.utils import get_random_secret_key
>> SECRET_KEY = get_random_secret_key()

OR 

SECRET_KEY = <ANY_50_CHARACTER_RANDOM_STRING>
```

### 4 Create .env file in project root

## Dev :
```python

# Settings - DEVELOPMENT
SECRET_KEY = SECRERT_KEY
DEBUG = True
ALLOWED_HOSTS = 127.0.0.1, localhost, [::1]

# White list domain 
CORS_ORIGIN_WHITELIST = http://localhost:3000, http://127.0.0.1:3000, http://127.0.0.1:19000

# Database
POSTGRES_USER = postgres
POSTGRES_PASSWORD = <password>
POSTGRES_DB = media_stream_local
POSTGRES_HOST = localhost
POSTGRES_PORT = 5432

# REDIS
CACHE_LOCATION = redis://localhost:6379/0
CELERY_BROKER_URL = redis://localhost:6379/1

# Timezone 
TIME_ZONE = Asia/Kolkata

# CELERY 
CELERY_RESULT_BACKEND = 'django-db'

# Google form 
GOOGLE_FORM_URL = <form_url>

WHATS_APP_LINK = <whats_app_url>
```
## Prod :
```json
# PRODUCTION

# Settings 
DEBUG= False
SECRET_KEY= django-insecure-..............
ALLOWED_HOSTS= localhost 127.0.0.1 web [::1]

# Postgres Database
POSTGRES_USER= postgres
POSTGRES_PASSWORD= <>
POSTGRES_DB= media_stream
POSTGRES_PORT= 5436
POSTGRES_HOST= database

# Postgres admin
PGADMIN_DEFAULT_EMAIL= <email>@gmail.com
PGADMIN_DEFAULT_PASSWORD= <>

#Django super user
# DJANGO_SUPERUSER_USERNAME= <email>
# DJANGO_SUPERUSER_EMAIL= <email>@gmail.com
# DJANGO_SUPERUSER_PASSWORD= <password>


# Redis
REDIS_HOST = redis://redis:6379/0
CACHE_LOCATION = redis://redis:6379/0

# Celery 
CELERY_BROKER_URL = redis://redis:6379/1
CELERY_RESULT_BACKEND = django-db

# Google form 
GOOGLE_FORM_URL = <form_url>

WHATS_APP_LINK = <url>

# Timezone 
TIME_ZONE = Asia/Kolkata

```
    

### 5. Docker 
```
# verify's docker compose syntax for erros.
> docker-compose config

# build docker image.
> docker-compose up

# rebuild image
> docker-compose up --build 
```

### 6. Open Docker and go to django image terminal
```
- Create admin user :
> python3.9 createsuperuser 

- Load Fixture Data :
> python3.9 manage.py loaddata ./video_app/data_backup/video_app_data.json
```

### 7. Running locally

```
> start wsl

> sudo service redis-server start

> start your postgres db

> python manage.py runserver
```