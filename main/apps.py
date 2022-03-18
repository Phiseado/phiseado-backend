from django.apps import AppConfig
from .services import url_model

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    model = url_model.UrlModel().model