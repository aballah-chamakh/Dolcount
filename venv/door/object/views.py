from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .serializers import ObjectSerializer
from .models import Object
# Create your views here.

class ObjectViewSet(ModelViewSet) :
    serializer_class = ObjectSerializer
    queryset = Object.objects.all()
    permissions_classes = [permissions.IsAdminUser]

    def perform_create(self,serializer):
        img = self.request.data['img']
        serializer.save(image=img)
