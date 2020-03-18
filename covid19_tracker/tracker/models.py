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

