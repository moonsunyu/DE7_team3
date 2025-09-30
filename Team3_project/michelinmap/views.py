from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.decorators.clickjacking import xframe_options_exempt

def index(request):
    return render(request, "michelinmap/index.html")


@xframe_options_exempt
def map_view(request):
    restaurants = list(Restaurant.objects.values("name", "latitude", "longitude"))
    context = {
        "restaurants": restaurants
    }
    return render(request, 'michelinmap/map.html', context)