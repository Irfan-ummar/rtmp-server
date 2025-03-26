#!/bin/bash

# Script to start an RTSP stream and convert it to RTMP
# Usage: ./start-stream.sh <camera_id> <rtsp_url>

if [ $# -lt 2 ]; then
    echo "Usage: $0 <camera_id> <rtsp_url>"
    echo "Example: $0 camera1 rtsp://username:password@camera-ip:554/stream"
    exit 1
fi

CAMERA_ID=$1
RTSP_URL=$2
RTMP_SERVER="rtmp://localhost:1935/live"
LOG_DIR="/var/log/cctv"
LOG_FILE="$LOG_DIR/ffmpeg-$CAMERA_ID.log"

# Create log directory if it doesn't exist
mkdir -p $LOG_DIR

# Kill any existing FFmpeg process for this camera
pkill -f "ffmpeg.*$CAMERA_ID"

echo "Starting stream for camera $CAMERA_ID..."
echo "RTSP URL: $RTSP_URL"
echo "RTMP destination: $RTMP_SERVER/$CAMERA_ID"

# Start FFmpeg in the background
ffmpeg -hide_banner -loglevel error \
    -rtsp_transport tcp \
    -i "$RTSP_URL" \
    -c:v copy -c:a aac -ar 44100 -ac 1 \
    -f flv "$RTMP_SERVER/$CAMERA_ID" > "$LOG_FILE" 2>&1 &

# Store the PID
PID=$!
echo $PID > "/tmp/ffmpeg-$CAMERA_ID.pid"

echo "Stream started with PID: $PID"
echo "Log file: $LOG_FILE"
echo "To stop the stream: ./stop-stream.sh $CAMERA_ID" 