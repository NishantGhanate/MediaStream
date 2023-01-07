
### Gunicron
```
gunicorn --bind :8000 --workers 3 media_stream.wsgi --capture-output

gunicorn --bind :8000 --workers 1  media_stream.wsgi \
--log-level=DEBUG \
--timeout=0 \
--access-logfile=-\
--log-file=-

gunicorn media_stream.wsgi  -c gunicorn.conf.py
```

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

### ffmeg - fprobe
> sudo apt install ffmpeg



> sudo apt install nginx 

> sudo nano /etc/systemd/system/gunicorn.socket
```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

> sudo nano /etc/systemd/system/gunicorn.service
```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/mnt/d/Github/MediaHls
ExecStart=/mnt/d/Github/MediaHls/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
           media_stream.wsgi:application

[Install]
WantedBy=multi-user.target


ps > wsl --shutdown

sudo systemctl enable gunicorn.socket

sudo systemctl start gunicorn.socket


sudo add-apt-repository ppa:nginx/stable
sudo apt-get install -y nginx
sudo service nginx start

sudo service gunicorn.socket start 
```


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

- https://pixabay.com/videos/search/small/