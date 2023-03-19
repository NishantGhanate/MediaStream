# MEDIA STREAM

A django web application to stream video content using .m3u8 


### System Requirements
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

### 3. Generate Django secret key :
```python
from django.core.management.utils import get_random_secret_key

get_random_secret_key()

'[SECRET KEY]'
```

### 4. Create .env file in project root
```python

# Settings
DEBUG= False
SECRET_KEY= sauce
ALLOWED_HOSTS= localhost 127.0.0.1 web [::1]

# Postgres Database
POSTGRES_USER= postgres
POSTGRES_PASSWORD= password
POSTGRES_DB= media_stream
POSTGRES_PORT= 5436
POSTGRES_HOST= database

# Postgres admin
PGADMIN_DEFAULT_EMAIL= abc@gmail.com
PGADMIN_DEFAULT_PASSWORD= cdef

# Redis
REDIS_HOST = redis://redis:6379/0
CACHE_LOCATION = redis://redis:6379/0

# Celery 
CELERY_BROKER_URL = redis://redis:6379/1
CELERY_RESULT_BACKEND = django-db

# Google form 
GOOGLE_FORM_URL = https://google.com

# Timezone 
TIME_ZONE = Asia/Kolkata
```

### 5. Docker 
docker-compose config
docker-compose up
docker-compose up --force-recreate