# MDBlogLite

**Stack**: Python, Django, PostgreSQL, Redis, Docker, Nginx, Celery

MDBlogLite allows you to deploy a simple blog where posts can be created using Markdown or HTML.

- The current release includes the ability to create posts, an "About Me" tab, and the standard Django admin panel for managing the author's account.
- With each new release, additional features will be added.

The goal of this application was defined as creating a simple blog for a single user, so it can be easily deployed on a low-resource VPS.
- In my case, a VPN was set up on the VPS, which also consumed its resources.
- You can think of this as a business card website with the capability to write posts.
- A blog with a more complex architecture will be available soon.

## Build Instructions

*Ensure Docker and the `make` utility are installed on the VPS.*

1. Run `make environment` -> This will create the `.env` file.
2. Run `make prepare` -> This will grant execution permissions to all necessary scripts.
3. Run `make webserver` -> This will set up the initial `nginx.conf` for configuring HTTPS certificates.
4. Run `make build` -> This will build the main application container.
5. Run `make up` -> This will start all containers.
6. Run `make secure` -> This will rewrite the `nginx.conf` for access via the HTTPS protocol.
7. Run `make restart` -> This will restart the web server after configuration changes.

## Environment Variables

All essential blog settings should be stored in the `.env` file located in the `env` directory.

* You can see an example structure in the `.env.template`.

```plaintext
BLOG_NAME=                       # The name of the blog
SITE_DOMAIN=                     # The domain name of the site
ADMIN_ENTRYPOINT=                # The entry point for the admin panel (example: www.domain.com/admin)
ADMIN_USERNAME=                  # The username for the admin account
ADMIN_EMAIL=                     # The email address for the admin account
ADMIN_PASSWORD=                  # The password for the admin account

DJANGO_ENV=production            # The environment setting for Django (production or development)
SECRET_KEY=                      # The secret key for Django
ALLOWED_HOSTS=                   # A comma-separated list of allowed hosts (example: example.org,localhost,12.23.345)

SESSION_COOKIE_SECURE=True       # Set to True for secure cookies over HTTPS
SESSION_COOKIE_AGE=              # The age of session cookies in seconds (When cookies expires, you will need re-login)
SESSION_COOKIE_HTTPONLY=True     # Set to True to prevent JavaScript access to cookies

RATE_LIMIT_VALUE=15              # Maximum number of requests allowed
RATE_LIMIT_WINDOW=3              # Time window (in minutes) for rate limiting
BAN_TIMEOUT=120                  # Time (in seconds) for banning an IP

POSTGRES_USER=                   # PostgreSQL database username
POSTGRES_PASSWORD=               # PostgreSQL database password
POSTGRES_DB=                     # Name of the PostgreSQL database
DB_HOST=                         # Hostname or IP address of the database server
DB_PORT=5432                     # Port number for the database connection

CACHE_DOMAIN=                    # Domain for the cache service
REDIS_PASSWORD=                  # Password for the Redis server
REDIS_PORT=6379                  # Port number for the Redis server
CACHE_TIMEOUT=                   # Cache timeout in seconds

SENTRY_STATUS=OFF                # Enable or disable Sentry error tracking (ON/OFF)
SENTRY_DSN=                      # Sentry DSN for error tracking

RECAPTCHA_SITEKEY=               # Your reCaptcha public sitekey
RECAPTCHA_SECRET=                # Your reCaptcha secret key
