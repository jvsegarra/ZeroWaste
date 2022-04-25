FROM python:3.10.4-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    vim \
    build-essential

RUN pip install --upgrade pip

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 8000

CMD ["uvicorn", "--reload", "--host=0.0.0.0", "--port=8000", "main:app"]
