from django.http import HttpResponse, JsonResponse
from django.template import loader

from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework import permissions

from .models import Location, CurrentLocation
from .serializers import LocationSerializer, CurrentLocationSerializer

from collections import OrderedDict
import json

from django.views.decorators.csrf import csrf_exempt

def index(request):
    current = CurrentLocation.objects.all()[0]
    x = current.x
    y = current.y
    yaw = current.yaw
    locations_list = Location.objects.all()
    locations_nearby = locations_list.filter(x__range=(x-1000, x+1000), y__range=(y-1000, y+1000)).all()
    locations_reached = locations_nearby.filter(x__range=(x-10, x+10), y__range=(y-10, y+10), yaw__range=(yaw-15, yaw+15)).all()
    template = loader.get_template('geoloc/index.html')
    context = {
        'locations_nearby': locations_nearby,
        'locations_reached': locations_reached,
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt 
def locations_list(request):
    if request.method == 'GET':
        current = CurrentLocation.objects.all()[0]
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        response = [{"x": current.x, "y": current.y, "yaw": current.yaw}] + json.loads(json.dumps(serializer.data))
        # print(response)
        return JsonResponse(response, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LocationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt 
def update_current_location(request):
    if request.method == 'GET':
        return HttpResponse(status=400)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CurrentLocationSerializer(data=data)
        current = CurrentLocation.objects.all()[0]

        if serializer.is_valid():
            serializer.update(current, serializer.validated_data)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
