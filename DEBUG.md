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