FROM python:3.11.8-bookworm as base

RUN apt-get update && apt-get install -y \
    fonts-microsoft-web-core \
    ttf-mscorefonts-installer

ENV PKGS_DIR=/install
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

FROM base as builder
RUN apt update
RUN apt install -y gcc g++
RUN pip install --upgrade pip

RUN mkdir $PKGS_DIR
RUN mkdir /app

WORKDIR /app

COPY systemart/requirements.txt /app/

# Install dependencies to local folder
RUN pip install --no-cache-dir --target=$PKGS_DIR -r ./requirements.txt
RUN pip install --no-cache-dir --target=$PKGS_DIR gunicorn

# Main image with service
FROM base
ARG SRC_PATH= /app

ENV PYTHONPATH=/usr/local
COPY --from=builder $PKGS_DIR /usr/local

COPY $SRC_PATH/systemart /app/systemart
WORKDIR /app/systemart

ENV SERVICE_DEBUG=False
ENV SERVICE_DB_PATH=/data
ENV SERVICE_HOST="0.0.0.0"
ENV SERVICE_PORT=8000

# Copying wait-for-it.sh inside the container
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN apt update && apt install -y dos2unix
RUN dos2unix /usr/local/bin/wait-for-it.sh

# Run service
CMD python manage.py makemigrations main && python manage.py migrate && gunicorn --workers=1 --bind $SERVICE_HOST:$SERVICE_PORT sysart.wsgi
