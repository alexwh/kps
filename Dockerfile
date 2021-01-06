FROM python:alpine

WORKDIR /app
# double negative is correct
ENV PIP_NO_CACHE_DIR=false

COPY Pipfile /app
COPY Pipfile.lock /app
RUN apk --no-cache add bash gcc musl-dev libffi-dev openssl-dev postgresql-dev git && \
    pip install pipenv && \
    pipenv sync && \
    apk del gcc musl-dev libffi-dev openssl-dev git

COPY . /app

# get proper pid1 reaping
ENTRYPOINT ["/app/run.sh"]
