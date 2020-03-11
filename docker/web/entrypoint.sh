#!/bin/bash

echo "---------pip install---------"
pip install -r /app/requirements.txt

exec "$@"
