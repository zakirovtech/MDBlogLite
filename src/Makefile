env:
	cp ./env/.env.template ./env/.env

prepare:
	chmod +x ./nginx/init.sh && chmod +x ./nginx/secure.sh

webserver:
	./nginx/init.sh

secure:
	./nginx/secure.sh
