FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p staticfiles media

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=wj_professionals.settings

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput --clear && gunicorn 'wj_professionals.wsgi:application' --bind 0.0.0.0:8000"]