# CCTV Camera Manager

A complete solution for managing IP cameras with RTMP streams, with support for streaming, recording, and monitoring CCTV cameras.

- Django backend with a REST API for camera management
- Nginx with RTMP module for HLS conversion
- Vue3 frontend that plays HLS streams using hls.js
- Swagger/ReDoc API documentation

## Features
- 📹 Direct RTMP streaming from IP cameras
- 📊 Camera management dashboard
- 🔄 Automatic stream conversion from RTMP to HLS
- 📱 Responsive UI for desktop and mobile viewing
- 🎯 On-demand recording and playback
- 🔒 Secure authentication
- 🔄 Health monitoring of camera streams

```
┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│   IP Camera  │        │     Nginx   │        │ Vue Frontend│
│  (RTMP src)  │───────▶│ RTMP→HLS   │───────▶│  (HLS.js)   │
└─────────────┘        └─────────────┘        └─────────────┘
                               │                      │
                               │                      │
                               │    ┌─────────────┐   │
                               └────│Django Backend│◀──┘
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
3. Enter the camera details:
   - Name: A descriptive name for the camera
   - IP Address: The IP address of your camera
   - RTMP Port: The RTMP port (default: 1935)
   - App Name: The RTMP application name (e.g., 'live')
   - Stream ID: The RTMP stream identifier
4. Choose whether to start streaming immediately
5. Save the camera

The RTMP URL will be automatically constructed in the format:
```
rtmp://{ip_address}:{rtmp_port}/{app_name}/{stream_id}
```

For example:
```
rtmp://192.168.1.100:1935/live/stream1
```

### Starting/Stopping Streams

- To start streaming a camera, click the "Start" button
- To stop a stream, click the "Stop" button
- Use the "Refresh" button to update the stream status

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

- **Stream not starting**: Check the camera's RTMP URL and credentials
- **Services not accessible**: Verify Docker is running and containers are up
- **"Connection refused" errors**: Ensure all services are running (check with `docker ps`)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Nginx-RTMP for the streaming server
- Django for the backend framework
- Vue.js for the frontend framework 