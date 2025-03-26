import subprocess
import logging
import os
import signal
from django.conf import settings

logger = logging.getLogger(__name__)

# Store running ffmpeg processes
ffmpeg_processes = {}

def start_stream(camera):
    """
    Start FFmpeg process to pull RTSP stream and push to RTMP server
    
    Args:
        camera: Camera model instance
    
    Returns:
        bool: True if stream started successfully, False otherwise
    """
    if camera.id in ffmpeg_processes and ffmpeg_processes[camera.id].poll() is None:
        logger.info(f"Stream for camera {camera.id} already running")
        return True
    
    rtsp_url = camera.rtsp_url
    
    # In Docker environment, we need to use the service name defined in docker-compose
    # Instead of localhost, use the Docker network service name
    rtmp_url = f"rtmp://rtmp_server:1935/live/{camera.id}"
    
    # Ensure the HLS directory exists
    hls_path = os.path.join(settings.HLS_ROOT, str(camera.id))
    os.makedirs(hls_path, exist_ok=True)
    
    # Set HLS URL for frontend to access
    # This should match the URL exposed by the RTMP server's HLS output
    camera.hls_url = f"{settings.HLS_BASE_URL}/{camera.id}/index.m3u8"
    camera.active = True
    camera.save()
    
    logger.info(f"Starting stream: {rtsp_url} -> {rtmp_url}")
    logger.info(f"HLS URL set to: {camera.hls_url}")
    
    try:
        # FFmpeg command to pull RTSP and push to RTMP
        command = [
            'ffmpeg',
            '-i', rtsp_url,
            '-c:v', 'copy',          # Copy video codec
            '-c:a', 'aac',           # Convert audio to AAC
            '-ar', '44100',          # Audio sample rate
            '-f', 'flv',             # Use FLV format for RTMP
            '-flvflags', 'no_duration_filesize',  # Avoid warnings
            rtmp_url
        ]
        
        # Log the full command for debugging
        logger.info(f"FFmpeg command: {' '.join(command)}")
        
        # Start FFmpeg process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        ffmpeg_processes[camera.id] = process
        logger.info(f"Started stream for camera {camera.id}: {rtsp_url} -> {rtmp_url}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to start stream for camera {camera.id}: {e}")
        camera.active = False
        camera.save()
        return False


def stop_stream(camera):
    """
    Stop FFmpeg stream process for a camera
    
    Args:
        camera: Camera model instance
    
    Returns:
        bool: True if stream stopped successfully, False otherwise
    """
    if camera.id not in ffmpeg_processes:
        logger.info(f"No stream process found for camera {camera.id}")
        return True
    
    process = ffmpeg_processes[camera.id]
    
    if process.poll() is None:  # Process is still running
        try:
            # Try to terminate gracefully
            process.terminate()
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # If it doesn't terminate, force kill
            process.kill()
        
        logger.info(f"Stopped stream for camera {camera.id}")
    
    # Remove from processes dict
    del ffmpeg_processes[camera.id]
    
    # Update camera status
    camera.active = False
    camera.save()
    
    return True


def restart_stream(camera):
    """
    Restart stream for a camera
    
    Args:
        camera: Camera model instance
    
    Returns:
        bool: True if stream restarted successfully, False otherwise
    """
    stop_stream(camera)
    return start_stream(camera)


def stop_all_streams():
    """Stop all running FFmpeg streams"""
    for camera_id, process in list(ffmpeg_processes.items()):
        if process.poll() is None:  # Process is still running
            try:
                process.terminate()
                process.wait(timeout=5)
            except (subprocess.TimeoutExpired, ProcessLookupError):
                process.kill()
            
            logger.info(f"Stopped stream for camera {camera_id}")
            
    ffmpeg_processes.clear()
    logger.info("All streams stopped") 