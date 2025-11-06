FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

RUN python manage.py collectstatic --noinput --clear

CMD exec gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120 --log-level=info