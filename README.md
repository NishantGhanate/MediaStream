# MEDIA STREAM

A django web application to stream video content using .m3u8 


### 1. Requirements
```
- Python 3.10
- Postgres Sql 14
- Windows 11
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

