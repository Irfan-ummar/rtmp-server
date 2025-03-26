from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CameraViewSet, RTMPCallbackView

router = DefaultRouter()
router.register(r'cameras', CameraViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stream/on_publish', RTMPCallbackView.as_view({'post': 'on_publish'})),
    path('stream/on_publish_done', RTMPCallbackView.as_view({'post': 'on_publish_done'})),
] 