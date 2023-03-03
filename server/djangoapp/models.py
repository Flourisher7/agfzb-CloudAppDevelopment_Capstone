
from django.db import models
from django.utils.timezone import now
from django.contrib import admin
from django.core import serializers 
import uuid
import json
# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=30, default='car make')
    description = models.CharField(max_length=1000, default='car make description')

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description

class CarModel(models.Model):
    SEDAN = 'SEDAN'
    SUV = 'SUV'
    WAGON = 'WAGON'
    TYPE_CHOICES = (
        (SEDAN, "SEDAN"),
        (SUV, "SUV"),
        (WAGON, "WAGON")
    )
    dealer_id = models.IntegerField(default=0)
    name = models.CharField(max_length=30, default='car model')
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default=SEDAN)
    year = models.DateField(default=now)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "DealerId: " + self.dealer_id.__str__() + "," + \
               "Type: " + self.type + "," + \
               "Year: " + self.year.__str__()

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
# class DealerReview:
class DealerReview:
    def __init__(
            self,
            dealership,
            name,
            purchase,
            review,
            # purchase_date,
            # another,
            # car_make,
            # car_model,
            # car_year,
            # sentiment,
            # id
    ):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        # self.purchase_date = purchase_date
        # self.another = another
        # self.car_make = car_make
        # self.car_model = car_model
        # self.car_year = car_year
        # self.sentiment = sentiment
        # self.id = id or 0

    def __str__(self):
        return "Review: " + self.review