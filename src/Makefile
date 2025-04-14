environment:
	cp ./env/.env.template ./env/.env

executeable:
	chmod u+x ./nginx/secure.sh && chmod u+x ./certbot/certbot-entrypoint.sh

site_secure:
	./nginx/secure.sh

build:
	docker compose -f docker-compose-production.yaml build --no-cache

up:
	docker compose -f docker-compose-production.yaml up -d

run_certbot:
	cd certbot 
	docker compose up
