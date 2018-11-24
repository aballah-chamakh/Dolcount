from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from .views import ObjectViewSet

router = routers.DefaultRouter()
router.register('object',ObjectViewSet)

urlpatterns = [
    path('', include(router.urls)),


]
