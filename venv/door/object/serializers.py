from .models import Object
from rest_framework import serializers

class ObjectSerializer(serializers.ModelSerializer):
    class Meta :
        model = Object
        fields = ('id','name','image','entered')
