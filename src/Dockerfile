FROM python:3.11-slim

WORKDIR /usr/app/src/

RUN apt-get update && apt-get upgrade -y

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /usr/app/src/scripts/

RUN chmod +x entrypoint.sh

WORKDIR /usr/app/src/

ENV PYTHONUNBUFFERED 1
