# Docker Setup for CCTV Camera Manager

This document explains how to run the CCTV Camera Manager application using Docker.

## Prerequisites

- Docker Engine
- Docker Compose

## Components

The application consists of three main Docker services:

1. **Backend (Django)**: Provides the REST API for camera management
2. **Frontend (Vue.js)**: Web interface for users to interact with the system
3. **RTMP Server (Nginx)**: Handles RTMP ingestion and HLS conversion

## Running the Application

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rtmp-server
   ```

2. Build and start all containers:
   ```bash
   docker-compose up -d
   ```

3. Create database migrations and apply them:
   ```bash
   docker-compose exec backend python manage.py makemigrations
   docker-compose exec backend python manage.py migrate
   ```

4. Create a superuser for admin access:
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

5. Access the application:
   - Frontend: http://localhost/
   - API Documentation: http://localhost/swagger/
   - Django Admin: http://localhost/admin/
   - Direct HLS Access: http://localhost:8080/hls/{camera_id}/index.m3u8
   - RTMP Server Simple Player: http://localhost:8080/

## Environment Variables

### Backend Environment Variables

The backend service uses the following environment variables:

- `DEBUG`: Set to "True" for development, "False" for production
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `HLS_BASE_URL`: URL for HLS streaming

You can modify these values in the `.env` file or directly in the `docker-compose.yml`.

## Port Mappings

- **Frontend**: Port 80
- **RTMP Server**: Ports 1935 (RTMP) and 8080 (HTTP)
- **Backend**: Not exposed directly (accessed through the frontend proxy)

## FFmpeg Command Example

To test the RTMP server with FFmpeg directly, you can use:

```bash
ffmpeg -re -i /path/to/video.mp4 -c copy -f flv rtmp://localhost:1935/live/1
```

Then access the HLS stream at: http://localhost:8080/hls/1/index.m3u8

## Volumes

The application uses Docker volumes to persist data:

- `backend_media`: Django media files including HLS segments
- `backend_static`: Django static files
- `hls_data`: HLS segments for the RTMP server

## Troubleshooting

1. **Database Issues**:
   ```bash
   docker-compose exec backend python manage.py makemigrations api
   docker-compose exec backend python manage.py migrate
   ```

2. **Permission Issues**:
   Check if container users have appropriate permissions for mounted volumes.

3. **Network Issues**:
   Ensure all services can communicate with each other on the `cctv_network`.

4. **Logs**:
   ```bash
   docker-compose logs -f backend
   docker-compose logs -f frontend
   docker-compose logs -f rtmp_server
   ```

## Useful Commands

- Stop all containers:
  ```bash
  docker-compose down
  ```

- Rebuild a specific service:
  ```bash
  docker-compose build <service_name>
  ```

- Restart a specific service:
  ```bash
  docker-compose restart <service_name>
  ```

- Shell access:
  ```bash
  docker-compose exec backend bash
  ```

- Django shell:
  ```bash
  docker-compose exec backend python manage.py shell
  ``` 