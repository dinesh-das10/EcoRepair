#!/usr/bin/env bash

python manage.py migrate
python manage.py seed_faults
python manage.py seed_centers