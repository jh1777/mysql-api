# --- using a prebuilt built-image, to forego caching ------------------------
FROM python:3.7-buster as poetry-build

RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
    build-essential libpq-dev python-pip libffi-dev python3-dev git curl zip && \
    pip install --upgrade pip && \
    apt-get clean && \
    apt-get purge -y

#ENV POETRY_VERSION=1.0.0b1 - use latest for now
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
ENV PATH="/root/.poetry/bin:${PATH}"

WORKDIR /app
COPY . .

RUN set -xe \
    && poetry build

# ----------------------------------------------------------------------------
FROM debian:buster-slim

ARG DEBIAN_FRONTEND=noninteractive

RUN set -xe \
    && apt-get update -q \
    && apt-get install -y gnupg wget \
    && apt-get update -q \
    && apt-get install -y -q --no-install-recommends \
    python3-minimal \
    python3-wheel \
    python3-pip \
    gunicorn3 \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /root/.cache \
    && rm -rf /var/lib/apt/lists/* \
    && useradd _gunicorn --create-home --home-dir /app --user-group

COPY --from=poetry-build /app/dist/*.whl .

RUN set -xe \
    && python3 -m pip install *.whl

USER _gunicorn
WORKDIR /app
COPY . .

# using multiple workers in order to guarantee successful health check when worker one is blocked
# set temp dir to /dev/shm, not using /tmp in container - it is slow
# redirect logfiles to stdout so docker/k8s can pull it

CMD ["gunicorn3", \
    "--preload", \
    "--bind", "0.0.0.0:8080", \
    "--worker-tmp-dir", "/dev/shm", \
    "--workers=2", "--threads=2", "--worker-class=gthread", \
    "--log-file=-", \
    "--timeout", "60",  \
    "app:api"]