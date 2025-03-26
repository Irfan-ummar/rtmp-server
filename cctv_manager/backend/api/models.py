from django.db import models

class Camera(models.Model):
    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    rtsp_port = models.IntegerField(default=554)
    stream_path = models.CharField(max_length=255, default='/live')
    hls_url = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def rtsp_url(self):
        return f"rtsp://{self.ip_address}:{self.rtsp_port}{self.stream_path}"
    
    @property
    def rtmp_url(self):
        return f"rtmp://localhost/live/{self.id}"
    
    def __str__(self):
        return self.name 