from django.shortcuts import render
from rest_framework.decorators import api_view
from michelinmap.models import Restaurant, Review, City, Region
from michelinmap_api.serializers import *
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.views import APIView


class RestaurantList(APIView):
    
    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     if request.method == 'POST':
    #         serializer = RestaurantSerializer(data=request.data)
    #     if serializer.is_valid(): # 놀랍게도 True, False만 반환하지 않고 validated_data도 저장함
    #         serializer.save()
    #         return Response(serializer.data, status=201)
    #     return Response(serializer.errors, status=400)

class RestaurantDetail(APIView):
    def get(self, request, pk):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            serializer = RestaurantSerializer(restaurant)
            return Response(serializer.data)
        except Restaurant.DoesNotExist:
            return Response(status=404)
    # def put(self, request, pk):
    #     try:
    #         restaurant = Restaurant.objects.get(pk=pk)
    #         serializer = RestaurantSerializer(restaurant, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=400)
    #     except Restaurant.DoesNotExist:
    #         return Response(status=404)
        
    # def delete(self, request, pk):
    #     try:
    #         restaurant = Restaurant.objects.get(pk=pk)
    #         restaurant.delete()
    #         return Response(status=204)
    #     except Restaurant.DoesNotExist:
    #         return Response(status=404)


class RegionList(APIView):
    def get(self, request):
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)
    
class CityList(APIView):
    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

class CityDetail(APIView):
    def get(self, request, pk):
        try:
            city = City.objects.get(pk=pk)
            serializer = CitySerializer(city)
            return Response(serializer.data)
        except City.DoesNotExist:
            return Response(status=404)
        
class ReviewList(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class ReviewDetail(APIView):
    def get(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist:
            return Response(status=404)


#===== 유저기능 구현 =====

# class RegisterUser(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer


#===== /유저기능 구현 =====
































# ---- 학습용 ----
# class RestaurantList():
#     def get(self, request):
#         restaurants = Restaurant.objects.all()
#         serializer = RestaurantSerializer(restaurants, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         if request.method == 'POST':
#             serializer = RestaurantSerializer(data=request.data)
#         if serializer.is_valid(): # 놀랍게도 True, False만 반환하지 않고 validated_data도 저장함
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

# class RestaurantDetail:
#     def get(self, request, pk):
#         try:
#             restaurant = Restaurant.objects.get(pk=pk)
#             serializer = RestaurantSerializer(restaurant)
#             return Response(serializer.data)
#         except Restaurant.DoesNotExist:
#             return Response(status=404)
#     def put(self, request, pk):
#         try:
#             restaurant = Restaurant.objects.get(pk=pk)
#             serializer = RestaurantSerializer(restaurant, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=400)
#         except Restaurant.DoesNotExist:
#             return Response(status=404)
        
#     def delete(self, request, pk):
#         try:
#             restaurant = Restaurant.objects.get(pk=pk)
#             restaurant.delete()
#             return Response(status=204)
#         except Restaurant.DoesNotExist:
#             return Response(status=404)

# @api_view(['GET', 'PUT', 'DELETE'])
# def restaurant_detail(request: Request, pk: int) -> Response:
#     if request.method == 'GET':
#         try:
#             restaurant = Restaurant.objects.get(pk=pk)
#             serializer = RestaurantSerializer(restaurant)
#             return Response(serializer.data)
#         except Restaurant.DoesNotExist:
#             return Response(status=404)

#     elif request.method == 'PUT':
#         try:
#             restaurant = Restaurant.objects.get(pk=pk)
#             serializer = RestaurantSerializer(restaurant, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=400)
#         except Restaurant.DoesNotExist:
#             return Response(status=404)

#     elif request.method == 'DELETE':
#         try:
#             restaurant = Restaurant.objects.get(pk=pk)
#             restaurant.delete()
#             return Response(status=204)
#         except Restaurant.DoesNotExist:
#             return Response(status=404)


