FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=$PYTHONPATH:/app:/app/app

RUN apt update -y && \
    apt install -y python3-dev gcc

RUN pip install poetry==1.1.7 && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY src/poetry.lock src/pyproject.toml /app/
ARG DEBUG=0
ARG TEST=0
RUN bash -c "\
if [[ \"$DEBUG\" == "1" || \"$TEST\" == "1"  ]] ; \
    then poetry install --no-root ; \
else \
    poetry install --no-root --no-dev ; \
fi"

# Cleanup trash
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
            gcc python3-dev && \
    rm -rf /var/lib/apt/lists/* /tmp/*

RUN mkdir /var/lib/plink
COPY src /app
RUN chmod -R u+x scripts/

RUN DJANGO_SETTINGS_MODULE="system.settings.build" \
    python manage.py collectstatic --noinput
