from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.decorators.clickjacking import xframe_options_exempt

def index(request):
    regions = list(Region.objects.values('id', 'r_name'))
    cities = list(City.objects.values('id', 'c_name', 'region_id'))

    city_id = request.GET.get('city_id')
    if city_id:
        restaurants = list(Restaurant.objects.filter(city_id=city_id)
                           .values('id', 'name', 'address', 'city_id'))
    else:
        restaurants = list(Restaurant.objects.values('id', 'name', 'address', 'city_id'))

    context = {
        'regions': regions,
        'cities': cities,
        'restaurants': restaurants,
        'selected_city_id': int(city_id) if city_id else None
    }
    return render(request, 'michelinmap/index.html', context)

@xframe_options_exempt
def map_view(request):
    restaurants = list(Restaurant.objects.values("name", "latitude", "longitude"))
    context = {
        "restaurants": restaurants
    }
    return render(request, 'michelinmap/map.html', context)