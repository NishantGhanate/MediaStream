# syntax=docker/dockerfile:1

FROM python:3.9

ADD . /app
WORKDIR /app

# Add base packages 
RUN apt-get update -y \
    && apt-get install software-properties-common -y\
    && apt-get install ffmpeg -y

RUN python3.9 -m pip install --upgrade setuptools

RUN python3.9 -m pip install -r requirements.txt

# copy our nginx configuration to overwrite nginx defaults
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 8000