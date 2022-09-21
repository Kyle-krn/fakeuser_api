FROM python:3.8
WORKDIR /fake_user_api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y


RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
COPY ./requirements.txt /fake_user_api/requirements.txt
RUN pip install -r requirements.txt

COPY . /fake_user_api


