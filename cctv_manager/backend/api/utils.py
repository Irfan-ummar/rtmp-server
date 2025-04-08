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
    Set up HLS streaming for a camera's RTMP stream
    
    Args:
        camera: Camera model instance
    
    Returns:
        bool: True if stream setup successfully, False otherwise
    """
    try:
        # Ensure the HLS directory exists
        hls_path = os.path.join(settings.HLS_ROOT, str(camera.id))
        os.makedirs(hls_path, exist_ok=True)
        
        # Set HLS URL for frontend to access
        # This should match the URL exposed by the RTMP server's HLS output
        camera.hls_url = f"{settings.HLS_BASE_URL}/{camera.id}/index.m3u8"
        camera.active = True
        camera.save()
        
        logger.info(f"Stream setup for camera {camera.id} - RTMP URL: {camera.rtmp_url}")
        logger.info(f"HLS URL set to: {camera.hls_url}")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to setup stream for camera {camera.id}: {e}")
        camera.active = False
        camera.save()
        return False


def stop_stream(camera):
    """
    Stop streaming for a camera
    
    Args:
        camera: Camera model instance
    
    Returns:
        bool: True if stream stopped successfully, False otherwise
    """
    try:
        # Update camera status
        camera.active = False
        camera.save()
        
        logger.info(f"Stopped stream for camera {camera.id}")
        return True
        
    except Exception as e:
        logger.error(f"Error stopping stream for camera {camera.id}: {e}")
        return False


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