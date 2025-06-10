# Create new Dockerfile
$content = @"
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start command
CMD ["gunicorn", "wj_professionals.wsgi:application", "--bind", "0.0.0.0:8000"]
"@

# Write the file
$content | Out-File -FilePath "Dockerfile" -Encoding utf8

# Create railway.toml
$railwayConfig = @"
[build]
builder = "dockerfile"
dockerfilePath = "Dockerfile"

[deploy]
startCommand = "gunicorn wj_professionals.wsgi:application --bind 0.0.0.0:8000"
"@

$railwayConfig | Out-File -FilePath "railway.toml" -Encoding utf8
