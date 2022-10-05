from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake (models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return ("Name : "+ self.name + "\nDescription : "+ self.description)
# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon')
    ]
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, primary_key=True)
    id = models.IntegerField()
    year = models.DateField(null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES,
        default=SEDAN)

    def __str__(self):
        return ("Name : "+ self.name + "\nID : "+ str(self.id) + "\nYear : "+ str(self.year) + "\nType : "+ self.type + "\nCarMake : "+ str(self.carmake))
    

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
