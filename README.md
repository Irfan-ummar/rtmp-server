# CCTV Camera Manager

A complete solution for managing IP cameras and RTMP streams, with support for streaming, recording, and monitoring CCTV cameras.

- Django backend with a REST API for camera management
- Nginx with RTMP module for converting RTMP streams to HLS
- FFmpeg for pulling RTSP streams from cameras and pushing to RTMP
- Vue3 frontend that plays HLS streams using hls.js
- Swagger/ReDoc API documentation

- 📹 Real-time streaming of RTSP cameras via RTMP and HLS
- 📊 Camera management dashboard
- 🔄 Automatic stream conversions from RTSP to RTMP
- 📱 Responsive UI for desktop and mobile viewing
- 🎯 On-demand recording and playback
- 🔒 Secure authentication
- 🔄 Health monitoring of camera streams

```
┌─────────────┐        ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│   IP Camera  │        │    FFmpeg   │        │     Nginx   │        │ Vue Frontend│
│  (RTSP src)  │───────▶│ RTSP→RTMP  │───────▶│ RTMP→HLS   │───────▶│  (HLS.js)   │
└─────────────┘        └─────────────┘        └─────────────┘        └─────────────┘
                               ▲                                            │
                               │                                            │
                               │          ┌─────────────┐                   │
                               └──────────│Django Backend│◀──────────────────┘
                                          │  REST API   │
                                          └─────────────┘
```

The application consists of three main components:

1. **Backend (Django)**: REST API for camera management
2. **Frontend (Vue.js)**: User interface for the camera dashboard
3. **RTMP Server (Nginx-RTMP)**: Handles video streaming with HLS support

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/cctv-manager.git
cd cctv-manager
```

2. Start the services
```bash
docker-compose up -d
```

3. Check the services status
```bash
./check-services.sh
```

### Accessing the Application

- **Frontend**: http://localhost/
- **Backend API**: http://localhost:8000/api/
- **API Documentation**: http://localhost:8000/swagger/
- **RTMP HLS Player**: http://localhost:8080/

## Usage

### Adding a Camera

1. Navigate to the dashboard
2. Click "Add Camera" button
3. Enter the RTSP URL of your camera (e.g., `rtsp://username:password@camera-ip:554/stream`)
4. Provide a name and location for the camera
5. Save the camera

### Starting/Stopping Streams

- To start streaming a camera, click the "Start" button
- To stop a stream, click the "Stop" button
- Use the "Restart" button to refresh the connection

### Viewing Streams

- Click on a camera tile to view its live stream
- The stream automatically uses HLS for playback

## Development

### Project Structure

```
cctv-manager/
├── backend/            # Django REST API
├── frontend/           # Vue.js frontend
├── nginx/              # Nginx configurations for the frontend
└── rtmp-server/        # NGINX-RTMP configuration
```

### Environment Variables

The following environment variables can be configured:

- `DJANGO_SECRET_KEY`: Django secret key
- `DJANGO_DEBUG`: Debug mode (True/False)
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string
- `RTMP_SERVER_URL`: URL of the RTMP server

## Troubleshooting

If you encounter issues with the system, use the provided `check-services.sh` script to verify the status of all services:

```bash
./check-services.sh
```

Common issues:

- **Stream not starting**: Check the camera's RTSP URL and credentials
- **Services not accessible**: Verify Docker is running and containers are up
- **"Connection refused" errors**: Ensure all services are running (check with `docker ps`)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Nginx-RTMP for the streaming server
- Django for the backend framework
- Vue.js for the frontend framework 