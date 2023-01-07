## imported Docker images from Hub.docker.com
FROM python:3.9.15-slim-bullseye

ENV PORT 8080

## Create Work dir

WORKDIR /app

## copy into  work dir

COPY . /app

## install required redundancies

RUN pip install -r requirement.txt

EXPOSE $PORT

CMD ["python","main.py"]


