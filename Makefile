
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USERNAME=example
export MYSQL_PASSWORD=test
export MYSQL_DB_NAME=habbitapp

run:
	python src/home.py

run_web:
	streamlit run src/home.py