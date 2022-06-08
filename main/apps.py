from django.apps import AppConfig
from .services import url_model, content_model

URL_model = None
CONTENT_model = None
class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        global URL_model
        global CONTENT_model

        URL_model = url_model.UrlModel().model
        CONTENT_model = content_model.ContentModel().model