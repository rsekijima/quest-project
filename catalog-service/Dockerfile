FROM python:3.10

ENV PYTHONPATH=/app

WORKDIR /app


COPY ./requirements.txt /app/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./scripts /app/scripts
COPY ./pyproject.toml  /app/
COPY ./app /app/app


CMD ["fastapi", "run", "app/main.py", "--port", "80"]