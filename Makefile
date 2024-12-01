
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USERNAME=example
export MYSQL_PASSWORD=test
export MYSQL_DB_NAME=habbitapp

run:
	python src/home.py

run_web:
	streamlit run src/home.py

test_run:
	python src/db_init.py

start_db:
	docker-compose -f docker-compose.yml up -d

stop_db:
	docker-compose -f docker-compose.yml down

start_test_db:
	docker-compose -f docker-compose.testing.yml up -d

stop_test_db:
	docker-compose -f docker-compose.testing.yml down

test:
	coverage run -m --source=src pytest
	coverage report -m
