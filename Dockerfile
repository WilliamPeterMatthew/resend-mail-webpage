FROM python:python:3.13.6-slim-trixie

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:5827", "app:app"]
