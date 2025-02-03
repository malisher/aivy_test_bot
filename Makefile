build_api:
	docker build -t doc.smartparking.kz/lp_recognizer_api:app api/

build_bot:
	docker build -t doc.smartparking.kz/lp_recognizer_bot:app telegram/

run:
	docker-compose up -d --build

stop:
	docker-compose down

restart:
	make stop
	make run

build_all:
	make build_api
	make build_bot

build_and_run:
	make build_all
	make run