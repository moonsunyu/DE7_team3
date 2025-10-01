from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from .models import *
from django.views.decorators.clickjacking import xframe_options_exempt

def index(request):

    region_id = request.GET.get('region_id')
    city_id = request.GET.get('city_id')

    # 전체 Region, City 목록 (드롭다운용)
    regions = list(Region.objects.values('id', 'r_name'))
    cities = list(City.objects.values('id', 'c_name', 'region_id'))

    restaurants_query = Restaurant.objects.none()
    restaurants = []

    if region_id or city_id:
        restaurants_query = Restaurant.objects.all()

        # 1. Region 필터링
        if region_id:
            try:
                region_id_int = int(region_id)
                restaurants_query = restaurants_query.filter(city__region_id=region_id_int)
            except ValueError:
                pass

        # 2. City 필터링
        if city_id and city_id != 'all':
            try:
                city_id_int = int(city_id)
                restaurants_query = restaurants_query.filter(city_id=city_id_int)
            except ValueError:
                pass

        restaurants = list(restaurants_query.values('id', 'name', 'address', 'category', 'city_id'))

    context = {
        'regions': regions,
        'cities': cities,
        'restaurants': restaurants,
        'selected_region_id': region_id,
        'selected_city_id': city_id,
    }

    return render(request, 'michelinmap/index.html', context)

@xframe_options_exempt
def map_view(request):
    region_id = request.GET.get('region_id')
    city_id = request.GET.get('city_id')

    restaurants = []

    # city_id가 존재할 때만 필터링
    if city_id:
        try:
            if city_id == 'all' and region_id:
                # region_id가 있을 때 → 해당 region에 속한 모든 city의 레스토랑
                region_id_int = int(region_id)
                restaurants = list(
                    Restaurant.objects.filter(city__region_id=region_id_int)
                    .values("name", "latitude", "longitude")
                )
            elif city_id != 'all':
                # 특정 city_id
                city_id_int = int(city_id)
                restaurants = list(
                    Restaurant.objects.filter(city_id=city_id_int)
                    .values("name", "latitude", "longitude")
                )
        except ValueError:
            pass

    context = {
        "restaurants": restaurants
    }
    return render(request, "michelinmap/map.html", context)


def detail(request, restaurant_id):
    # 기본키(pk)가 restaurant_id인 Restaurant 객체 가져오기
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

    context = {
        'restaurant': restaurant
    }
    return render(request, 'michelinmap/detail.html', context)