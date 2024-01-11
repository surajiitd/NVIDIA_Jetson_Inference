from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Location(models.Model):
    location_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    voice_message = models.CharField(default='You have reached ', max_length=200)
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    yaw = models.FloatField(default=0.0, validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])

    def __str__(self) -> str:
        return self.location_name

class CurrentLocation(models.Model):
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    yaw = models.FloatField(default=0.0, validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])

    def __str__(self) -> str:
        return '( ' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.yaw) + ' )'
