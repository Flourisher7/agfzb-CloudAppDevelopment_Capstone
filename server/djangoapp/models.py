from django.db import models
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid

class CarMake(models.Model):
    # id = models.BigAutoField(primary_key=True)
    name = models.CharField(null = False, max_length=25)
    description = models.CharField(null = True, max_length=500)

    def __str__(self):
        return 'Name:' + self.name + ',' + 'Description: ' + self.description

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30)
    SEDAN = "Sedan"
    SUV = "SUV"
    WAGON = "Wagon"
    LIMOUSINE = "Limousine"
    BATMOBILE = "Batmobile"
    CAR_TYPES = [(SEDAN, "Sedan"), (SUV, "SUV"), (WAGON, "Wagon"),
                (LIMOUSINE, "Limousine"), (BATMOBILE, "Batmobile")]

    car_type = models.CharField(null=False, max_length=20, choices=CAR_TYPES)
    year = models.DateField()
    dealer_id = models.IntegerField()
    year = models.DateField()

    def __str__(self):
        return "Name: "+ self.name + \
                " Make Name: "+ self.make.name + \
                " Type: " + self.car_type + \
                " Dealer ID: " + str(self.dealer_id)+ \
                " Year: " + str(self.year)


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
