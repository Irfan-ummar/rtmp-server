FROM python:3.9-slim

WORKDIR /app

# Install system dependencies including FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create media and static directories with proper permissions
RUN mkdir -p /app/media/hls && \
    mkdir -p /app/static && \
    chmod -R 777 /app/media && \
    chmod -R 777 /app/static

# Collect static files
RUN python manage.py collectstatic --noinput

# Create startup script
RUN echo '#!/bin/bash\n\
python manage.py collectstatic --noinput\n\
python manage.py makemigrations\n\
python manage.py migrate\n\
exec gunicorn cctv_manager.wsgi:application --bind 0.0.0.0:8000 --workers 2\n\
' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Create a non-root user and change ownership
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the Django development server port
EXPOSE 8000

# Command to run the application
CMD ["/app/entrypoint.sh"] 