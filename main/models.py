from django.db import models
from main.services.url_model import UrlModel
from datetime import datetime, timedelta
class Message(models.Model):
    url = models.URLField()
    registered_date = models.DateTimeField(auto_now_add=True)
    considered_phishing = models.BooleanField(default=False)   

    domain = models.ForeignKey('Domain', on_delete=models.CASCADE)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)

    def __str__(self):
        return self.url + " " + str(self.registered_date)

class Domain(models.Model):
    name = models.CharField(max_length=255)
    frequency = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " " + str(self.frequency)

class Country(models.Model):
    name = models.CharField(max_length=255)
    country_iso_code = models.CharField(max_length=255)

    def __str__(self):
        return self.name + " " + self.country_iso_code

class Retrain(models.Model):
    retrain_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.retrain_date)

    def save(self, *args, **kwargs):
        global URL_model
        new_messages = Message.objects.filter(registered_date__gt=datetime.now() - timedelta(days=30))
        URL_model = UrlModel().retrain_url_model(new_messages)
        super().save(*args, **kwargs)