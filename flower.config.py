# management api
broker_api = 'redis://localhost:6379/1'

# Enable debug logging
logging = 'DEBUG'


# celery  --app media_stream  flower --broker=redis://localhost:6379/1 --port=5566

# celery --app media_stream flower --port=5566

# celery  --config=flower.config.py flower