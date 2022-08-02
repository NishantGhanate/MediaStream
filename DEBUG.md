git config --global core.autocrlf true


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
```

### ffmeg - fprobe
> sudo apt install ffmpeg