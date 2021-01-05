FROM python:slim

WORKDIR /app

RUN pip install pipenv
COPY Pipfile /app
COPY Pipfile.lock /app
RUN pipenv sync

COPY . /app

# get proper pid1 reaping
ENTRYPOINT ["/app/run.sh"]
