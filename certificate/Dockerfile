FROM python:3.10

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update &&  pip install --upgrade pip 

COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt
COPY ./certificate /usr/src/app

EXPOSE 8000



