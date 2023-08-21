FROM python:3.9-alpine3.13
LABEL maintainer='Hongdong Bao'

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false

# Use only 1 single RUN command to avoid create layers to make the image lightweight
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # install postgresql client in the image as a dependency for psycopg2
    apk add --update --no-cache postgresql-client && \
    # sets an virtual dependency package, groups packages we install into .tmp-build-deps, can use this to remove packages later inside our docker file
    apk add --update --no-cache --virtual .tmp-build-deps \
        # these are the packages we need to install and group into .tmp-build-deps
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = 'true' ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user