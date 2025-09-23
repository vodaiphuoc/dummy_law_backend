#!/bin/sh
set -e

# Fallback to plain HTTP if certs are not provided
if [ -z "$SSL_PATH" ] || [ -z "$SSL_ROOT_PATH" ]; then
    exec uvicorn main:app --host 0.0.0.0 --port 8080
else
    echo "$SSL_PATH"
    ls "$SSL_PATH"
    ls "$SSL_ROOT_PATH"
    exec uvicorn main:app \
        --host 0.0.0.0 \
        --port "$AUTHEN_PORT" \
        --log-level debug \
        --ssl-certfile "$SSL_PATH/authen.crt" \
        --ssl-keyfile "$SSL_PATH/authen.key" \
        --ssl-ca-certs "$SSL_ROOT_PATH/ca.crt" \
        --ssl-cert-reqs 2
fi
