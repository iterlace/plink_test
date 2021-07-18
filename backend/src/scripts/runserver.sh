#!/bin/bash

if [ "$DEBUG" = "0" ]; then
  echo "Running in production mode (gunicorn)...";
  gunicorn src.wsgi:application\
    -w "$GUNICORN_WORKERS" \
    --bind :8000 \
    --reload  \
    --timeout=${GUNICORN_TIMEOUT:-240} \
    --graceful-timeout=60 \
    --log-level=DEBUG;
else
  echo "Running in development mode (default Django runner)...";
  python /app/manage.py runserver 0.0.0.0:8000;
fi;
