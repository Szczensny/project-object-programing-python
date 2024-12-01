FROM python:3.10

RUN apt-get update && apt-get install make -y
RUN mkdir /app
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT [ "streamlit", "run", "src/home.py", "--server.port", "8080" ]