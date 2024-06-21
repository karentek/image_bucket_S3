# FROM python:3.11
# RUN apt-get update -qq && apt-get install -y -qq \
#     gdal-bin binutils libproj-dev libgdal-dev cmake &&\
#     apt-get clean all &&\
#     rm -rf /var/apt/lists/* &&\
#     rm -rf /var/cache/apt/*
# ENV PYTHONUNBUFFERED 1
# WORKDIR /django_app
# COPY . /django_app
# RUN pip install poetry && \
#     poetry config virtualenvs.create false && \
#     poetry install
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh



FROM python:3.11 as base

ENV PKGS_DIR=/install \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

FROM base as builder

RUN pip install --upgrade pip
RUN pip install poetry

RUN apt update
RUN mkdir $PKGS_DIR

RUN mkdir /code
WORKDIR /code

COPY poetry.lock pyproject.toml /code/
RUN poetry export --without-hashes -f requirements.txt --output ./requirements.txt
RUN pip install --target=$PKGS_DIR -r ./requirements.txt

# Install dependencies to local folder
RUN pip install --target=$PKGS_DIR -r ./requirements.txt
RUN pip install --target=$PKGS_DIR gunicorn

# Main image with service
FROM base

RUN apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/usr/local
COPY --from=builder /install /usr/local

WORKDIR /app
COPY ./app /app

ENV SERVICE_HOST="0.0.0.0"
ENV SERVICE_PORT=8000

# Run service
CMD python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --workers=1 --bind $SERVICE_HOST:$SERVICE_PORT hardqode.wsgi
EXPOSE 8000