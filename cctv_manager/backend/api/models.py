from django.db import models

class Camera(models.Model):
    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    rtmp_port = models.IntegerField(default=1935)
    app_name = models.CharField(max_length=255, default='live')
    stream_id = models.CharField(max_length=255, default='stream1')
    hls_url = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def rtmp_url(self):
        return f"rtmp://{self.ip_address}:{self.rtmp_port}/{self.app_name}/{self.stream_id}"
    
    def __str__(self):
        return self.name 