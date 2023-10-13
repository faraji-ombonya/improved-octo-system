from rest_framework import serializers
from .models import Enroll, Recognize

class EnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enroll
        fields = '__all__'
    
class RecognizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recognize
        fields = '__all__'
        