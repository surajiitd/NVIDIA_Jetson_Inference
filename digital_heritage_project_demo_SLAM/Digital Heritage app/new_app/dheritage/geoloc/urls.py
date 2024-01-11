from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('locations/', views.locations_list, name='list'),
    path('updatecurrent/', views.update_current_location, name='update'),
]
