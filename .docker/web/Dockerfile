FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN pip install --upgrade pip

ADD requirements.txt .
RUN apt update \
    && apt install -y postgresql-client libpq-dev \
    && pip install -r requirements.txt \
    && python -m playwright install --with-deps chromium
