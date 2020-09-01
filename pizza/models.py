from django.db import models


# Create your models here.
class Size(models.Model):
    title = models.CharField(max_length=100)
    cost = models.FloatField()

    def __str__(self):
        return self.title


class Crust(models.Model):
    type = models.CharField(max_length=100)
    cost = models.FloatField()

    def __str__(self):
        return self.type


class Topping(models.Model):
    name = models.CharField(max_length=100)
    cost = models.FloatField()

    def __str__(self):
        return self.name


class Pizza(models.Model):
    toppings = models.ManyToManyField(Topping)
    crust = models.ForeignKey(Crust, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def toppings_as_string(self):
        return ', '.join(self.toppings)
