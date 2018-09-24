#!/bin/bash

if [ ! "$1" != "" ]; then
    echo "Missing 1 argument - path to certificate! Exiting."
    exit 1
fi


CERT_PATH=$(awk -F "=" '/cert_path / {print $2}' auth.config.ini | tr -d ' ')
CERT_KEY_PATH=$(awk -F "=" '/cert_key_path / {print $2}' auth.config.ini | tr -d ' ')

openssl pkcs12 -in $1 -clcerts -nokeys -out $HOME/$CERT_PATH
openssl pkcs12 -in $1 -nocerts -out $HOME/$CERT_KEY_PATH
