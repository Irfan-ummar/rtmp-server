from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Camera
from .serializers import CameraSerializer
from .utils import start_stream, stop_stream, restart_stream
import logging

logger = logging.getLogger(__name__)

class CameraViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cameras to be viewed or edited.
    """
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    
    @swagger_auto_schema(
        operation_description="Start the RTSP to RTMP stream for a camera",
        responses={
            200: openapi.Response(
                description="Stream started successfully",
                examples={
                    "application/json": {
                        "status": "stream started"
                    }
                }
            ),
            500: "Failed to start stream"
        }
    )
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start the RTSP to RTMP stream for a camera"""
        camera = self.get_object()
        success = start_stream(camera)
        
        if success:
            return Response({'status': 'stream started'}, status=status.HTTP_200_OK)
        return Response({'status': 'failed to start stream'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_description="Stop the RTSP to RTMP stream for a camera",
        responses={
            200: openapi.Response(
                description="Stream stopped successfully",
                examples={
                    "application/json": {
                        "status": "stream stopped"
                    }
                }
            ),
            500: "Failed to stop stream"
        }
    )
    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        """Stop the RTSP to RTMP stream for a camera"""
        camera = self.get_object()
        success = stop_stream(camera)
        
        if success:
            return Response({'status': 'stream stopped'}, status=status.HTTP_200_OK)
        return Response({'status': 'failed to stop stream'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_description="Restart the RTSP to RTMP stream for a camera",
        responses={
            200: openapi.Response(
                description="Stream restarted successfully",
                examples={
                    "application/json": {
                        "status": "stream restarted"
                    }
                }
            ),
            500: "Failed to restart stream"
        }
    )
    @action(detail=True, methods=['post'])
    def restart(self, request, pk=None):
        """Restart the RTSP to RTMP stream for a camera"""
        camera = self.get_object()
        success = restart_stream(camera)
        
        if success:
            return Response({'status': 'stream restarted'}, status=status.HTTP_200_OK)
        return Response({'status': 'failed to restart stream'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RTMPCallbackView(viewsets.ViewSet):
    """
    API endpoints for RTMP server callbacks
    """
    
    def on_publish(self, request):
        """
        Callback from Nginx RTMP server when a stream starts publishing
        """
        try:
            stream_name = request.data.get('name', '')
            app = request.data.get('app', '')
            
            logger.info(f"Stream publish started - app: {app}, name: {stream_name}")
            
            # Try to find the camera by id (stream name)
            try:
                camera_id = int(stream_name)
                try:
                    camera = Camera.objects.get(id=camera_id)
                    camera.active = True
                    camera.save()
                    logger.info(f"Camera {camera_id} marked as active")
                except Camera.DoesNotExist:
                    logger.warning(f"Camera with ID {camera_id} not found")
            except ValueError:
                # Not a numeric camera ID
                logger.warning(f"Non-numeric stream name: {stream_name}")
            
            # Always return 200 to allow publishing
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in on_publish callback: {e}")
            # Always return 200 to allow publishing even in case of errors
            return Response({'status': 'Error'}, status=status.HTTP_200_OK)
    
    def on_publish_done(self, request):
        """
        Callback from Nginx RTMP server when a stream stops publishing
        """
        try:
            stream_name = request.data.get('name', '')
            app = request.data.get('app', '')
            
            logger.info(f"Stream publish ended - app: {app}, name: {stream_name}")
            
            # Try to find the camera by id (stream name)
            try:
                camera_id = int(stream_name)
                try:
                    camera = Camera.objects.get(id=camera_id)
                    camera.active = False
                    camera.save()
                    logger.info(f"Camera {camera_id} marked as inactive")
                except Camera.DoesNotExist:
                    logger.warning(f"Camera with ID {camera_id} not found")
            except ValueError:
                # Not a numeric camera ID
                logger.warning(f"Non-numeric stream name: {stream_name}")
            
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in on_publish_done callback: {e}")
            return Response({'status': 'Error'}, status=status.HTTP_200_OK) 