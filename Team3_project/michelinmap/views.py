from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from .models import *
from django.views.decorators.clickjacking import xframe_options_exempt
from django.db.models import Count
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Hannanum
import base64
from io import BytesIO

def index(request):

    region_id = request.GET.get('region_id')
    city_id = request.GET.get('city_id')

    # 전체 Region, City 목록 (드롭다운용)
    regions = list(Region.objects.values('id', 'r_name'))
    cities = list(City.objects.values('id', 'c_name', 'region_id'))

    restaurants_query = Restaurant.objects.none()
    restaurants = []

    if region_id and city_id:
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

        restaurants = list(restaurants_query.values('id', 'name', 'address', 'category', 'city_id', 'page', 'price'))

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
    region_id_param = request.GET.get('region_id')
    city_id_param = request.GET.get('city_id')

    restaurants = []

    # city_id가 존재할 때만 필터링
    if city_id_param:
        try:
            if city_id_param == 'all' and region_id_param: # 전체 선택
                region_id_int = int(region_id_param)
                restaurants = list(
                    Restaurant.objects.filter(city__region_id=region_id_int)
                    .values("name", "latitude", "longitude")
                )
            elif city_id_param != 'all': # 특정 city 선택
                city_id_int = int(city_id_param)
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
    # 식당 객체 가져오기
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    reviews = Review.objects.filter(restaurant=restaurant)

    if restaurant.rating == "None":
        restaurant.rating = None

    # 별점 비율 계산
    total_reviews = reviews.count()
    rating_counts = reviews.values('star').annotate(count=Count('star'))
    star_dict = {i: 0 for i in range(1, 6)}
    for r in rating_counts:
        if total_reviews > 0:
            star_dict[r['star']] = r['count'] / total_reviews

    # 워드 클라우드 생성
    good_reviews = []
    bad_reviews = []
    hannanum = Hannanum()

    for review in reviews:
        text = review.comment  # 리뷰 텍스트
        nouns = [noun for noun in hannanum.nouns(text) if len(noun) > 1]  # 명사 추출
        if review.star >= 3:
            good_reviews.extend(nouns)
        else:
            bad_reviews.extend(nouns)

    def create_wordcloud(counter):
        if not counter:  # 단어가 없으면 None 반환
            return None
        wordcloud = WordCloud(
            font_path="michelinmap/static/michelinmap/fonts/Pretendard-Regular.ttf",
            background_color="white",
            width=300,
            height=300
        )
        wordcloud.generate_from_frequencies(counter)
        buffer = BytesIO()
        wordcloud.to_image().save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return img_str

    good_wc = create_wordcloud(Counter(good_reviews))
    bad_wc = create_wordcloud(Counter(bad_reviews))

    context = {
        'restaurant': restaurant,
        'star_ratio': star_dict,
        'good_wc': good_wc,
        'bad_wc': bad_wc,
    }

    return render(request, 'michelinmap/detail.html', context)