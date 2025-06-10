# Create optimized Dockerfile
@"
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for static files and media
RUN mkdir -p staticfiles media

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=wj-professionals.settings

# Expose port
EXPOSE 8000

# Start command with migrations and static files
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput --clear && gunicorn wj_professionals.wsgi:application --bind 0.0.0.0:8000"]
"@ | Out-File -FilePath Dockerfile -Encoding utf8 -NoNewline
