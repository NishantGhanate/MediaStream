#!/bin/bash

echo -e "\e[34m >>> Creating migration files \e[97m"
# python3.9 manage.py makemigrations

echo -e "\e[34m >>> Migrating changes \e[97m"
python3.9 manage.py migrate
echo -e "\e[32m >>> migration completed \e[97m"

echo -e "\e[34m >>> Collecting Static files \e[97m"
# python3.9 manage.py collectstatic --noinput
echo -e "\e[32m >>> Static files collect completed \e[97m"

echo -e "\e[32m >>> Running server \e[97m"
gunicorn -c gunicorn.conf.py media_stream.wsgi:application
