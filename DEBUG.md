
### 1. Python setup 
```
- sudo add-apt-repository ppa:deadsnakes/ppa
- sudo apt install python3.9
- python3.9 --version
- curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
- python3.9 get-pip.py
- sudo apt-get install python3.9-distutils
- python3.9 -m pip --version
- python3.9 -m pip install virtualenv
- python3.9 -m virtualenv venv
- pip --version
- apt-get -y install libz-dev libjpeg-dev libfreetype6-dev python-dev
```

### 2. Project Setup 
```
- git clone https://github.com/NishantGhanate/MediaStream.git
- cd MediaStream
- python3.9 -m virtualenv venv
- source venv/bin/activate
- pip install -r requirements.txt 
```

### 3. Generate Django secret key :
```python
from django.core.management.utils import get_random_secret_key

get_random_secret_key()

'[SECRET KEY]'
```


### 5. Run server
```
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver 0.0.0.0:8000
```

### 5.1 Dump / load json data
```
- python manage.py dumpdata video_app > ./video_app/data_backup/video_app_data.json

- python manage.py loaddata ./video_app/data_backup/video_app_data.json

```
<hr>

## 6. Celery Setup
```
In order to use celery we need to setup 

Option 1 : 6.1 & 6.2
- Redis

OR 

OPtion 2 :
- Erlang
- RabbitMQ on windows 
```

### 6.1 Redis & Celery Setup
```
Open another wsl terminal 
- sudo apt-get install redis
- sudo service redis-server start
- redis-cli 
- PING

EXtra : Redis GUI 

- Redis on wsl 2
- redisInsight-v2 [https://redis.com/redis-enterprise/redis-insight/#insight-form]

```


### 6.2 Run Celery : sh start_celery.sh
```
celery --app media_stream worker -l info --pool=solo

<syntax> 
celery --app <project_name> worker -l info --pool=solo
celery -A media_stream worker -l INFO
celery -A media_stream worker -l info -Q celery, high
celery -A media_stream worker -l INFO -Q celery,high  --pool=solo

```
Note : Make to sure to run migration if you have installed celery later


<hr>

### 6.3 Rabbit MQ
Using Chocolatey (power shell on admin mode):
> choco install rabbitmq

OR 

Install mannually 


### 6.3.1 Erlang : https://www.erlang.org/downloads
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

### 6.3.2 RabbitMQ : https://www.rabbitmq.com/install-windows.html
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

### 7. Celery Flower : To visualize tasks status
```

This is the template to follow:

> celery [celery args] flower [flower args]

> celery -A media_stream flower --port=5566

```

### 8. Install ffmeg & nginx
> sudo apt install ffmpeg

> sudo add-apt-repository ppa:nginx/stable

> sudo apt-get install -y nginx
`

### Gunicron Django server 
```
1. Default Run
> python manage.py collectstatic
> gunicorn media_stream.wsgi  -c gunicorn.conf.py

2. Cli Run
> sudo -s
> gunicorn --bind :8000 --workers 3 media_stream.wsgi --capture-output

3. Extra keywords
> gunicorn --bind :8000 --workers 3  media_stream.wsgi \
--log-level=DEBUG \
--timeout=0 \
--access-logfile=-\
--log-file=-

```

### 9. Production setup :

1. Create guicorn socket config
> sudo nano /etc/systemd/system/media_stream_gunicorn.socket
```
[Unit]
Description=media stream gunicorn socket connection

[Socket]
ListenStream=/run/media_stream_gunicorn.sock

[Install]
WantedBy=sockets.target
```

2. Create guincorn socket service
> sudo nano /etc/systemd/system/media_stream_gunicorn.service
```
Group=www-data
WorkingDirectory=/mnt/d/Github/MediaHls
ExecStart=/mnt/d/Github/MediaHls/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/media_stream_gunicorn.sock \
           media_stream.wsgi:application

[Install]
WantedBy=multi-user.target
```
2. Start guicorn 
> sudo service media_stream_gunicorn.socket start
> sudo service media_stream_gunicorn.socket enable
> sudo media_stream_gunicorn.socket status

3. Set permission
> sudo chown -R www-data:root /mnt/d/Github/MediaHls

4. Restart wsl using powershell in admin mode
> wsl --shutdown

5. Create nginx config
> sudo nano /etc/nginx/conf.d/media_stream.conf

```
copy contents from project/ngix/media_stream
```

6. Copy to site-enabled
> sudo cp /etc/nginx/conf.d/media_stream.conf /etc/nginx/sites-enabled/

7. Test nginx configsu
> sudo nginx -t

> sudo /etc/init.d/nginx start

> sudo /etc/init.d/nginx reload

> sudo /etc/init.d/nginx restart

> sudo /etc/init.d/nginx status

## NOTE : 
using windows to host server from wsl make sure IISM is not using same port

### Dump & Load Model data
```
python manage.py dumpdata video_app.LanguageModel  > ./video_app/data_backup/model_name.json
python manage.py loaddata ./video_app/data_backup/model_name.json
```

### Migration
```
python manage.py migrate video_app 0002_languagemodel

python manage.py migrate --fake video_app 0002_languagemodel

or 
Take table data backup and clear migration log of speific model
DELETE FROM public.django_migrations
WHERE id= 37;

```




ps > wsl --shutdown

sudo systemctl enable gunicorn.socket

sudo systemctl start gunicorn.socket

sudo service gunicorn.socket start 


### GIT 
```
Since we are working on wsl to keep git same across we will use autocrlf true 
in windows & wsl as well .

1. See existing mode 
> git config --get core.autocrlf

2 Set autocrlf true in gitbash & wsl terminal
> git config --global core.autocrlf true

```

### TEST SMALL VIDEOS
```

- https://pixabay.com/videos/search/small/

- https://arctype.com/blog/install-django-ubuntu/

```

# 
- https://raw.githubusercontent.com/nginx/nginx/master/conf/nginx.conf


sudo nano /etc/nginx/conf.d/test.conf

  server {
    listen        8005;
    server_name   localhost;
    error_log     /mnt/d/Github/MediaHls/logs/nginx-error.log;
  
    location /static/  {
      autoindex    on;
      alias /mnt/d/Github/MediaHls/static/;
    }

}


cd /var/log/nginx
sudo  nginx -c /etc/nginx/conf.d/test.conf -t

> sudo /etc/init.d/nginx start
> sudo /etc/init.d/nginx configtest

> sudo cp /etc/nginx/conf.d/test.conf /etc/nginx/sites-enabled/

# backup config
> sudo cp /etc/nginx/sites-enabled/default.conf /etc/nginx/conf.d/

> cd /etc/nginx/sites-enabled/

> sudo /etc/init.d/nginx restart

- http://127.0.0.1:8005/static/static/images/banner-bg.png
- 

- cat /var/log/nginx/error.log

> cd /var/www/html;
> sudo nano index.nginx-debian.html


https://stackoverflow.com/questions/41766195/nginx-emerg-server-directive-is-not-allowed-here

- https://kifarunix.com/create-locally-trusted-ssl-certificates-with-mkcert-on-ubuntu-20-04/
