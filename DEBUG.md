
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
