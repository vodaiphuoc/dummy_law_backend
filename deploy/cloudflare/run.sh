#!/bin/bash

TAG=v0.1

CURRENT_FILE_DIR=$(dirname "$(realpath "$0")")
PROJECT_DIR=$(dirname $(dirname $(dirname "$(realpath "$0")")))

# option to run
OPTS=$(getopt -o "" --long front-end-certs-path:,root-sub:,nginx-service-name:,authen-service-name: -- "$@")
eval set -- "$OPTS"

# nginx
NGINX_IMAGE=nginx:1.25
NGINX_CONTAINER=chatbot-nginx

# authen FASTAPI service
AUTHEN_IMAGE=chatbot-authen-image:$TAG
AUTHEN_CONTAINER=chatbot-authen
AUTHEN_PORT=8443

# make env file for docker compose
cat <<EOF > "$CURRENT_FILE_DIR/.env"
NGINX_IMAGE=$NGINX_IMAGE
NGINX_CONTAINER=$NGINX_CONTAINER
AUTHEN_IMAGE=$AUTHEN_IMAGE
AUTHEN_CONTAINER=$AUTHEN_CONTAINER
AUTHEN_PORT=$AUTHEN_PORT
EOF

bash $CURRENT_FILE_DIR/gen-certs.sh \
    --root-sub $4 \
    --nginx-service-name $6 \
    --authen-service-name $8

# copy frontend certs
if [ -z "$(ls $CURRENT_FILE_DIR/certs/frontend)" ]; then
    # ls $CURRENT_FILE_DIR/certs/frontend
    cp -r $PROJECT_DIR/$2 $CURRENT_FILE_DIR/certs/
fi

chmod -R 775 "$CURRENT_FILE_DIR/certs"

# clean up
cleanup() {
  echo "Runining cleanup ..."
  # The cleanup commands you already have
  docker container rm -f "$NGINX_CONTAINER" "$AUTHEN_CONTAINER"
  docker image rm -f "$AUTHEN_IMAGE"
  
  echo "Cleanup complete."
  exit 1
}
trap cleanup SIGINT

# run docker compose
docker compose \
  --env-file "$CURRENT_FILE_DIR/.env" \
  -f "$CURRENT_FILE_DIR/Docker-compose.yaml" \
  up --abort-on-container-exit --build
