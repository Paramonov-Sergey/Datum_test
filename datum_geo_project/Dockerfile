FROM python:3.9.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/datum_geo_app_dir

COPY ./requerements.txt /usr/src/requerements.txt

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin

RUN pip install -r /usr/src/requerements.txt

COPY . /usr/src/datum_geo_app_dir

EXPOSE 8000
