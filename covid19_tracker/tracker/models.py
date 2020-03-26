from django.db import models

# Create your models here.

class Date(models.Model):
    date = models.DateField("date")
    confirmed = models.IntegerField("confirmed_cases")
    deaths = models.IntegerField("deaths")
    recovered = models.IntegerField("recovered_cases")
    country = models.CharField(max_length=200) 

    def __str__(self):
        return str(self.date) + ": in: "+ self.country+": confirmed: "+ str(self.confirmed)+ ", deaths: "+ str(self.deaths)+", recovered: "+ str(self.recovered)

    time = models.TimeField("time")
    confirmed = models.IntegerField("confirmed_cases")
    deaths = models.IntegerField("deaths")
    new_cases = models.IntegerField("new_cases")
    new_deaths = models.IntegerField("new_deaths")
    mortality = models.FloatField("mortality")
    country = models.CharField(max_length=200) 

