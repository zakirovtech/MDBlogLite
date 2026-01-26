# MDBlogLite — запуск на VPS (Production)

Данный гайд описывает пошаговый запуск блога MDBlogLite на VPS с использованием:

* Docker + Docker Compose

* отдельного Nginx в Docker

* Certbot (Let’s Encrypt)

* общей Docker-сети nginx_network

## 0. Предварительные требования

Перед началом убедитесь, что у вас есть:

VPS с Linux (рекомендуется Ubuntu / AlmaLinux)

Установлены:

* docker

* docker compose

* Арендован домен

* DNS A-запись домена указывает на IP вашего VPS

* Открыты порты 80 и 443 (firewalld / ufw)

1. Клонирование репозитория
```git clone https://github.com/zakirovtech/MDBlogLite.git
cd MDBlogLite
```
2. Настройка переменных окружения

Перейдите в папку с env-файлами и создайте .env:

```cd src/env
cp .env.template .env
```

Заполните все обязательные (refill) переменные, вот пример:
```
APP=MDBlogLite
DOCKER_SERVICE_NAME=web
BLOG_NAME=refill
SITE_DOMAIN=refill
ADMIN_ENTRYPOINT=refill
ADMIN_USERNAME=refill
ADMIN_EMAIL=refill valid email
ADMIN_PASSWORD=refill

DJANGO_ENV=production
SECRET_KEY=refill strong string
ALLOWED_HOSTS=refill your domains

SESSION_COOKIE_SECURE=True
SESSION_COOKIE_AGE=3600
SESSION_COOKIE_HTTPONLY=True

RATE_LIMIT_VALUE=15
RATE_LIMIT_WINDOW=3
BAN_TIMEOUT=120
RATE_LIMIT_WINDOW_SECONDS=120

POSTGRES_USER=refill
POSTGRES_PASSWORD=refill
POSTGRES_DB=mdbloglite
DB_HOST=db
DB_PORT=5432

CACHE_DOMAIN=cache
REDIS_PASSWORD=refill
REDIS_PORT=6379
CACHE_TIMEOUT=120

SENTRY_STATUS=OFF
SENTRY_DSN=

RECAPTCHA_SITEKEY=
RECAPTCHA_SECRET=

ENABLE_DEBUG_TOOLBAR=
```

После этого вернитесь в корень проекта:

`cd ..`

## 3. Подготовка домена

Убедитесь, что:

* домен уже арендован

* A-запись домена указывает на IP VPS

* DNS изменения применились (обычно до 10–15 минут)

Проверка:

`ping your-domain.com`

## 4. Подготовка Nginx (в Docker)

Nginx работает отдельно от приложения, в своей Docker-сети nginx_network.

### 4.1 Создание Docker-сети (один раз)
`docker network create nginx_network || true
`
### 4.2 Пример docker-compose для Nginx
```version: '3.7'

services:
  nginx:
    image: nginx:latest
    container_name: system-nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /opt/nginx/conf.d:/etc/nginx/conf.d
      - /opt/nginx/allowlists:/etc/nginx/allowlists
      - /opt/nginx/logs:/var/log/nginx/
      - /opt/certbot/www:/var/www/certbot/:ro
      - /opt/certbot/conf/:/etc/nginx/ssl/:ro

      # Static / media of applications
      - /home/<user>/MDBlogLite/src/media/:/MDBlogLite/media/
      - /home/<user>/MDBlogLite/src/static/:/MDBlogLite/static/
    networks:
      - nginx_network

networks:
  nginx_network:
    driver: bridge
    name: nginx_network

```
Запустите nginx:

`docker compose up -d`

## 5. Создание HTTP-конфига для Certbot

Из папки **src** выполните:

```sudo nginx/certbot.sh
```

Скрипт:

* создаст HTTP-конфиг nginx

* файл будет в /opt/nginx/conf.d/

* имя файла содержит домен (например **certbot.example.com.conf**)

* добавит /.well-known/acme-challenge/

## 6. Перезагрузка Nginx
```docker exec system-nginx nginx -t
docker exec system-nginx nginx -s reload
```
## 7. Получение SSL-сертификата (Certbot)

Перейдите в папку certbot и запустите контейнер:
```
cd src/certbot
docker compose up
```

Certbot:

* проверит доступность домена

* выпустит сертификат Let’s Encrypt

* сохранит его в /opt/certbot/conf/

После успешного получения контейнер можно остановить.

## 8. Запуск web-приложения

Вернитесь в корень проекта:

`cd ../..`


Запустите production-сборку приложения:

`docker compose -f docker-compose-production.yaml up -d --build`

Убедитесь, что контейнер web работает и находится в сети nginx_network.

## 9. Создание HTTPS-конфига Nginx

Запустите secure-скрипт:

`sudo nginx/secure.sh`


Скрипт:

* создаст HTTPS-сервер

* подключит сертификаты

* настроит proxy на web:8000

* подключит static и media

* Конфиг будет создан в /opt/nginx/conf.d/.

## 10. Финальная перезагрузка Nginx
docker exec system-nginx nginx -t
docker exec system-nginx nginx -s reload

✅ Готово

Теперь блог доступен по адресу:

https://your-domain.com

Примечания

* Nginx и приложение должны быть в одной Docker-сети

* Certbot использует HTTP (порт 80) только для выпуска/обновления сертификатов

* HTTPS работает постоянно через nginx

* Все nginx-конфиги и сертификаты лежат вне проекта, в /opt

## Переменные окружения (.env) — описание
```
# Общие

APP — имя приложения/папки, используется в nginx-конфигах (пути к /APP/static и /APP/media).

DOCKER_SERVICE_NAME — имя сервиса в docker-compose, на который nginx проксирует (обычно web).

BLOG_NAME — название блога (используется в админке/шапках/титулах).

SITE_DOMAIN — основной домен сайта (например example.com), используется в nginx и certbot.

ADMIN_ENTRYPOINT — путь к админке Django (например admin/ или super-secret-admin/).

# Админ-пользователь (инициализация)

ADMIN_USERNAME — логин администратора (superuser).

ADMIN_EMAIL — email администратора (superuser) + используется certbot (если также применяется как контакт).

ADMIN_PASSWORD — пароль администратора (superuser).

Django / Security

DJANGO_ENV — окружение (production, development), влияет на выбор настроек.

SECRET_KEY — секретный ключ Django (обязательно сильный, уникальный).

ALLOWED_HOSTS — список разрешённых хостов (домены и/или IP через запятую).

# Cookies / Sessions

SESSION_COOKIE_SECURE — ставить cookie только по HTTPS (True для прод).

SESSION_COOKIE_AGE — время жизни сессии в секундах.

SESSION_COOKIE_HTTPONLY — запрет доступа к cookie из JS (True рекомендуется).

Rate limiting / Ban (защита от брута/спама)

RATE_LIMIT_VALUE — сколько запросов/попыток разрешено за окно.

RATE_LIMIT_WINDOW — размер окна (используется вместе со следующей переменной; см. реализацию).

BAN_TIMEOUT — время бана в секундах.

RATE_LIMIT_WINDOW_SECONDS — размер окна rate limit в секундах.

Примечание: у тебя одновременно есть RATE_LIMIT_WINDOW и RATE_LIMIT_WINDOW_SECONDS. Лучше оставить одну (секунды) — но это зависит от того, как именно ты используешь их в коде.

# PostgreSQL (prod)

POSTGRES_USER — пользователь БД Postgres.

POSTGRES_PASSWORD — пароль пользователя БД.

POSTGRES_DB — имя базы данных.

DB_HOST — хост базы (в docker-compose обычно db).

DB_PORT — порт Postgres (обычно 5432).

# Redis / Cache

CACHE_DOMAIN — хост Redis/кэша (в docker-compose обычно cache).

REDIS_PASSWORD — пароль Redis (если включена авторизация; если нет — оставить пустым или выключить в конфиге).

REDIS_PORT — порт Redis (обычно 6379).

CACHE_TIMEOUT — TTL по умолчанию для кэша (секунды).

# Sentry (ошибки)

SENTRY_STATUS — включить/выключить sentry (ON/OFF).

SENTRY_DSN — DSN проекта Sentry (строка подключения).

# reCAPTCHA

RECAPTCHA_SITEKEY — публичный ключ reCAPTCHA (вставляется на клиенте).

RECAPTCHA_SECRET — секретный ключ reCAPTCHA (проверка на сервере).

Debug

ENABLE_DEBUG_TOOLBAR — включение Django Debug Toolbar (только для dev; в prod должно быть пусто/False).
```