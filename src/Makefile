environment:
	cp ./env/.env.template ./env/.env

prepare:
	chmod +x ./nginx/init.sh && chmod +x ./nginx/secure.sh && chmod +x ./certbot/init.sh

webserver:
	./nginx/init.sh

build:
	docker compose -f docker-compose-production.yaml build --no-cache

up:
	docker compose -f docker-compose-production.yaml up -d

secure:
	./nginx/secure.sh

restart:
	docker compose -f docker-compose-production.yaml restart nginx
