
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
	python src/main.py

test:
	docker-compose -f docker-compose.testing.yml up -d
	coverage run -m --source=src pytest 
	coverage report -m
	docker-compose -f docker-compose.testing.yml down