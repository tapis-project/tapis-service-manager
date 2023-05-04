FROM python:3.10-slim

RUN apt-get update

RUN apt-get install -y vim git

RUN mkdir src

COPY src/requirements.txt /src/requirements.txt

WORKDIR /src

RUN pip install -r requirements.txt

COPY src/ /src