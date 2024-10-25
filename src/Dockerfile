FROM python:3.11-slim

WORKDIR /usr/app/src/

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONDONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y
RUN apt install gettext -y

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /usr/app/src/scripts/

RUN chmod +x entrypoint.sh \
    && chmod +x wait-for-it.sh \
    && chmod +x create_superuser.sh

WORKDIR /usr/app/src/
