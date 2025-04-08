from rest_framework import serializers
from .models import Camera

class CameraSerializer(serializers.ModelSerializer):
    """
    Serializer for the Camera model.
    """
    rtmp_url = serializers.ReadOnlyField(
        help_text="Computed RTMP URL for the camera stream"
    )
    
    class Meta:
        model = Camera
        fields = ['id', 'name', 'ip_address', 'rtmp_port', 'app_name', 
                 'stream_id', 'hls_url', 'rtmp_url', 'active', 
                 'created_at', 'updated_at']
        read_only_fields = ['hls_url', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'help_text': 'A descriptive name for the camera'},
            'ip_address': {'help_text': 'IP address of the camera'},
            'rtmp_port': {'help_text': 'RTMP port of the camera (default: 1935)'},
            'app_name': {'help_text': 'RTMP application name (e.g., live)'},
            'stream_id': {'help_text': 'RTMP stream ID'},
            'hls_url': {'help_text': 'URL to the HLS stream (auto-generated)'},
            'active': {'help_text': 'Whether the camera stream is currently active'},
        } 