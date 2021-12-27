FROM python:3.7.12
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN apt update && apt install -y memcached libmemcached-dev && pip install -r requirements.txt
ADD . /code/
