# Habit app
Habit app is a web based aplication that allows you to track your own habbits.
The application comes with the example dataset for 4 weeks. 
If you want to not load it - in file `docker-compose.yml` please uncoment line `30`.

This project can be runned localy - directly form the computer enviroment or by using Docker Compose.
Habit app have two components.
1) MySQL database that is in the form of the docker containers
2) Streamlit application that can be run as part of the user system or in docker containers

**IMPORTANT**

By default data is not presistent in the setup. If you want to save it on your disk as well in the file `docker-compose.yml` please uncomment lines `11` and `12`.

## Requirements
**Docker** - for building containers for the application

**Docker Compose** - for orchestrating services

**Make File** - for easy access to comands 

## Starting application

### Docker version (recommended)
In your terminal please use command

```
docker-compose -f docker-compose.yml up 
```
That will start the MySQL database and the streamlit app. After loading you can access aplication in your webbrowser under link http://localhost:8080

To stop application please use:
```
docker-compose -f docker-compose.yml down
```

### Local instalation
The application can be also run directly from the user computer enviroment, but what is recommented to use still python virtual enviroment. In the example belowe it is used the conda enviroment

Setup of the enviroment:
```
conda create -n habit_app PYTHON=3.10
conda activate habit_app
pip install -r requirements.txt
```
Starting Application:
```
## only if enviroment is not active already
conda activate habit_app 

make start_db
## OR
docker-compose -f docker-compose.yml up -d db

make run_web
## OR
streamlit run src/home.py --server.port 8080
```
Usage of Makefile depends on the user decision.

Stoping application:
```
## Stoping Streamlint app - ctrl + c

## Stoping DB
make stop_db
## OR
docker-compose -f docker-compose.yml down
```

## Application usage


## Running Tests
Application came with the test that are checking the correctnes of the outcomes for functions build-into app. If you want to run them please follow steps below:

### Running in docker

Simply run commend:
```
docker-compose -f docker-compose.testing.yml up
```

After test run you can remove containers and test dadtabase by:
```
docker-compose -f docker-compose.testing.yml down
```

### Running localy

Prepare enviroment:
```
conda create -n habit_app_test PYTHON=3.10
conda activate habit_app_test
pip install -r requirements_dev.txt
```

Running tests
```
## Start test DB
docker-compose -f docker-compose.testing.yml up -d db_test
## OR
make start_test_db

coverage run -m --source=src pytest
coverage report -m
## OR
make test
```

To stop and remove test DB and its container:
```
docker-compose -f docker-compose.testing.yml down
```