from django.urls import path
from . import views

app_name = 'michelinmap'
urlpatterns = [
    path('',views.index, name='index'),
    path('map/', views.map_view, name='map'),
    path('<int:restaurant_id>/', views.detail, name='detail'), # 상세 페이지
]