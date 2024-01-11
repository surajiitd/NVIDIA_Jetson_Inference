from rest_framework import serializers
from .models import Location, CurrentLocation

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ['location_name', 'description', 'voice_message', 'x', 'y', 'yaw']

class CurrentLocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CurrentLocation
        fields = ['x', 'y', 'yaw']
