#!/bin/bash
CURRENT_FILE_DIR=$(dirname "$(realpath "$0")")
set -e

# option to run
OPTS=$(getopt -o "" --long root-sub:,nginx-service-name:,authen-service-name: -- "$@")
eval set -- "$OPTS"

CERTS_DIR="$CURRENT_FILE_DIR/certs"

NGINX_SER_DIR="$CERTS_DIR/$4"
AUTHEN_SER_DIR="$CERTS_DIR/$6"

mkdir -p $CERTS_DIR
mkdir -p $CERTS_DIR/root
mkdir -p $NGINX_SER_DIR
mkdir -p $AUTHEN_SER_DIR

# 0. Create OpenSSL config with SANs for authen-service only
cat > "$AUTHEN_SER_DIR/openssl.cnf" <<EOF
[ req ]
default_bits       = 2048
distinguished_name = req_distinguished_name
req_extensions     = v3_req
x509_extensions    = v3_req
prompt             = no

[ req_distinguished_name ]
CN = $6

[ v3_req ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = $6
DNS.2 = localhost
IP.1  = 127.0.0.1
IP.2  = 0.0.0.0
EOF

# 1. Root CA
openssl genrsa -out $CERTS_DIR/root/ca.key 4096
openssl req -x509 -new -nodes \
    -key $CERTS_DIR/root/ca.key \
    -sha256 -days 365 \
    -out $CERTS_DIR/root/ca.crt \
    -subj "$2"

# 2. Nginx cert
openssl genrsa -out $NGINX_SER_DIR/nginx.key 2048
openssl req -new \
    -key $NGINX_SER_DIR/nginx.key \
    -out $NGINX_SER_DIR/nginx.csr \
    -subj "/CN=$4"

openssl x509 -req \
    -in $NGINX_SER_DIR/nginx.csr \
    -CA $CERTS_DIR/root/ca.crt \
    -CAkey $CERTS_DIR/root/ca.key \
    -CAcreateserial \
    -out $NGINX_SER_DIR/nginx.crt \
    -days 365 -sha256

# 3. authen cert
openssl genrsa -out $AUTHEN_SER_DIR/authen.key 2048
openssl req -new \
    -key $AUTHEN_SER_DIR/authen.key \
    -out $AUTHEN_SER_DIR/authen.csr \
    -subj "/CN=$6" \
    -config "$AUTHEN_SER_DIR/openssl.cnf"

openssl x509 -req \
    -in $AUTHEN_SER_DIR/authen.csr \
    -CA $CERTS_DIR/root/ca.crt \
    -CAkey $CERTS_DIR/root/ca.key \
    -CAcreateserial \
    -out $AUTHEN_SER_DIR/authen.crt \
    -days 365 -sha256 \
    -extensions v3_req \
    -extfile "$AUTHEN_SER_DIR/openssl.cnf"

echo "✅ Dev certificates generated in $CERTS_DIR"
