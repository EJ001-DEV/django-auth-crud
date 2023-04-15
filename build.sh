#!/usr/bin/env bash
# exit on error
set -o errexit

#no se necesita poetry
#poetry install
#pip install -r requirements.txt
#pip install --upgrade pip

python manage.py collectstatic --no-input
python manage.py migrate