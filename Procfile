web: gunicorn -b :$PORT -w 8 wsgi:application
worker: celery worker -A celery_app.application -l INFO
