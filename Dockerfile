# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY requirements.prod requirements.prod
RUN pip3 install -r requirements.prod
RUN apt-get -y update
RUN apt-get -y install git

COPY . .

CMD [ "python3", "-m" , "streamlit", "run", "nlapp/app.py", "--server.port", "8502"]
