from rest_framework import serializers
from .models import Camera

class CameraSerializer(serializers.ModelSerializer):
    """
    Serializer for the Camera model.
    """
    rtsp_url = serializers.ReadOnlyField(
        help_text="Computed RTSP URL based on the camera's IP, port, and stream path"
    )
    rtmp_url = serializers.ReadOnlyField(
        help_text="Computed RTMP URL for the stream on the RTMP server"
    )
    
    class Meta:
        model = Camera
        fields = ['id', 'name', 'ip_address', 'rtsp_port', 'stream_path', 
                 'hls_url', 'rtsp_url', 'rtmp_url', 'active', 
                 'created_at', 'updated_at']
        read_only_fields = ['hls_url', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'help_text': 'A descriptive name for the camera'},
            'ip_address': {'help_text': 'IP address of the camera'},
            'rtsp_port': {'help_text': 'RTSP port of the camera (default: 554)'},
            'stream_path': {'help_text': 'Stream path on the camera (e.g., /live)'},
            'hls_url': {'help_text': 'URL to the HLS stream (auto-generated)'},
            'active': {'help_text': 'Whether the camera stream is currently active'},
        } 