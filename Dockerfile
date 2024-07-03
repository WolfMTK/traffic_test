FROM python:3.12

COPY src src

COPY pyproject.toml pyproject.toml

RUN pip install .

CMD uvicorn --factory app.main:start_app --host 0.0.0.0 --port 8000
