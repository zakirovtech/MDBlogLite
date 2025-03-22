environment:
	cp ./env/.env.template ./env/.env

prepare:
	chmod +x ./nginx/secure.sh && chmod +x ./certbot/init.sh

webserver:
	./nginx/secure.sh

build:
	docker compose -f docker-compose-production.yaml build --no-cache

up:
	docker compose -f docker-compose-production.yaml up -d

certbot:
	./certbot/init.sh
