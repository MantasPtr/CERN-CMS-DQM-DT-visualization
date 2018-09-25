#!/bin/bash
set -e

if [ ! "$1" != "" ]; then
    echo "Missing 1 argument - path to certificate! Exiting."
    exit 1
fi

# read auth.config.ini files
CERT_PATH=$(awk -F "=" '/cert_path / {print $2}' auth.config.ini | tr -d ' ')
CERT_KEY_PATH=$(awk -F "=" '/cert_key_path / {print $2}' auth.config.ini | tr -d ' ')

# extract certificatesopenssl pkcs12 -in $1 -clcerts -nokeys -out $HOME/$CERT_PATH
openssl pkcs12 -in $1 -clcerts -nokeys -out $HOME/$CERT_PATH
openssl pkcs12 -in $1 -nocerts -out __temp_file.userkey_encrypted.pem
openssl rsa -in __temp_file.userkey_encrypted.pem -out $HOME/$CERT_KEY_PATH
rm __temp_file.userkey_encrypted.pem
chmod go-rw $HOME/$CERT_KEY_PATH
