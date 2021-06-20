FROM python:3.9.2-slim

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN pip install pipenv

COPY Pipfile /tmp
COPY Pipfile.lock /tmp
WORKDIR /tmp
RUN pipenv install --system && rm -rf /tmp/*

WORKDIR /