from django.contrib import admin

from .models import Message, Domain, Country, Retrain

admin.site.register(Message)
admin.site.register(Domain)
admin.site.register(Country)
admin.site.register(Retrain)
