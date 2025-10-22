from rest_framework import serializers
from michelinmap.models import Restaurant, Review, City, Region
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

# class RegionSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     r_name = serializers.CharField(max_length=100)


#     def create(self, validated_data):
#         return Region.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.r_name = validated_data.get("r_name", instance.r_name)
#         instance.save()
#         return instance
    
# class CitySerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     c_name = serializers.CharField(max_length=100)
#     region = RegionSerializer(read_only=True)

#     def create(self, validated_data):
#         return City.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.c_name = validated_data.get("c_name", instance.c_name)
#         instance.save()
#         return instance
    


# class RestaurantSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=200)
#     address = serializers.CharField(max_length=300)
#     city = CitySerializer(read_only=True)
#     latitude = serializers.FloatField()
#     longitude = serializers.FloatField()
#     category = serializers.CharField(max_length=100)
#     page = serializers.CharField(max_length=300)
#     price = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
#     rating = serializers.FloatField(allow_null=True)
#     review_cnt = serializers.IntegerField(allow_null=True)
#     call_number = serializers.CharField(max_length=20, allow_null=True, allow_blank=True)
#     def create(self, validated_data):
#         return Restaurant.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get("name", instance.name)
#         instance.address = validated_data.get("address", instance.address)
#         instance.save()
#         return instance
    
# class ReviewSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     rating = serializers.IntegerField()
#     comment = serializers.CharField(max_length=500)
#     restaurant = RestaurantSerializer(read_only=True)

#     def create(self, validated_data):
#         return Review.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.rating = validated_data.get("rating", instance.rating)
#         instance.comment = validated_data.get("comment", instance.comment)
#         instance.save()
#         return instance

# ================= ModelSerializer로 변경 ==================
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'r_name']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'c_name', 'region']

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'city', 'latitude', 'longitude', 'category', 'page', 'price', 'rating', 'review_cnt', 'call_number']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'star', 'comment', 'restaurant']

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})
#         return attrs
    
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'password2']
