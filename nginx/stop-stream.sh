#!/bin/bash

# Script to stop an RTSP to RTMP stream
# Usage: ./stop-stream.sh <camera_id>

if [ $# -lt 1 ]; then
    echo "Usage: $0 <camera_id>"
    echo "Example: $0 camera1"
    exit 1
fi

CAMERA_ID=$1
PID_FILE="/tmp/ffmpeg-$CAMERA_ID.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    echo "Stopping stream for camera $CAMERA_ID (PID: $PID)..."
    
    # Send SIGTERM signal to the process
    if kill -15 $PID 2>/dev/null; then
        echo "Stream stopped successfully."
    else
        echo "Process doesn't exist. Trying to find and kill the process..."
        if pkill -f "ffmpeg.*$CAMERA_ID"; then
            echo "Found and stopped ffmpeg process for camera $CAMERA_ID."
        else
            echo "No running ffmpeg process found for camera $CAMERA_ID."
        fi
    fi
    
    # Remove PID file
    rm -f "$PID_FILE"
else
    echo "PID file not found. Trying to find and kill the process..."
    if pkill -f "ffmpeg.*$CAMERA_ID"; then
        echo "Found and stopped ffmpeg process for camera $CAMERA_ID."
    else
        echo "No running ffmpeg process found for camera $CAMERA_ID."
    fi
fi

# Notify that HLS fragments will remain until they expire
echo "Note: HLS fragments will remain in the cache until they expire according to the server configuration." 