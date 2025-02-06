web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
web: daphne -b 0.0.0.0 -p 8080 myproject.asgi:application

