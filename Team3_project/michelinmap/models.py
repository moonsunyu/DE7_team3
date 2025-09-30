from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    latitude = models.FloatField()
    longitude = models.FloatField()
    category = models.CharField(max_length=100)
    rating = models.FloatField(blank=True, null=True)
    call_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    star = models.FloatField(blank=True)
    comment = models.TextField(blank=True, default='')

    def __str__(self):
        return str(self.star)

class Region(models.Model):
    r_name = models.CharField(max_length=100)

    def __str__(self):
        return self.r_name

class City(models.Model):
    c_name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.c_name