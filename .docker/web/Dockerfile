FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN pip install --upgrade pip

ADD requirements.txt .
RUN apt update \
    && apt install -y memcached libmemcached-dev \
    && pip install -r requirements.txt
