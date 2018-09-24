#!/bin/bash


if [ ! "$1" != "" ]; then
    echo "Please provide path to certificate"
    exit 1
fi

openssl pkcs12 -in $1 -nocerts -out key.pem
openssl pkcs12 -in $1 -clcerts -nokeys -out cert.pem