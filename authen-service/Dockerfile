FROM python:3.10-slim-bullseye

WORKDIR /app

COPY ./authen-service/*.* .
COPY ./authen-service/static ./static
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV SSL_PATH="" \
    SSL_ROOT_PATH=""\
    AUTHEN_PORT=8000

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]