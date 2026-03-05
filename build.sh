#!/usr/bin/env bash

set -o errexit

pip install -r requirements/prod.txt

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username=os.environ.get('SUPERUSER_NAME')).exists():
    User.objects.create_superuser(os.environ.get('SUPERUSER_NAME'), os.environ.get('SUPERUSER_EMAIL'), os.environ.get('SUPERUSER_PASSWORD'))
"