web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn sortmaster.wsgi --bind 0.0.0.0:$PORT
