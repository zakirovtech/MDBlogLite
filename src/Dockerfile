FROM python:3.11-slim

WORKDIR /usr/app/src/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONDONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gettext \
        libcairo2 libcairo2-dev \
        libpango-1.0-0 libpango1.0-dev \
        libgdk-pixbuf-2.0-0 libgdk-pixbuf-2.0-dev \
        libfreetype6 libfreetype6-dev \
        fontconfig \
    && rm -rf /var/lib/apt/lists/*


COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /usr/app/src/scripts/

RUN chmod +x entrypoint.sh \
    && chmod +x wait-for-it.sh \
    && chmod +x create_superuser.sh

WORKDIR /usr/app/src/
