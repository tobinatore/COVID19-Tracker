from django.db import models

# Create your models here.

class Date(models.Model):
    date = models.DateField("date")
    confirmed = models.IntegerField("confirmed_cases")
    deaths = models.IntegerField("deaths")
    recovered = models.IntegerField("recovered_cases")

    def __str__(self):
        return str(self.date)

class Country(models.Model):
    name = models.CharField(max_length=200)
    date = models.ForeignKey(Date, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name
