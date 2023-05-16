from django.contrib import admin
from django.apps import apps
from .models import *
app_config = apps.get_app_config('tours')

#Те модели которые не нужно регистрировать!!! Их нужно импортнуть отдельно
NOT_REGISTERED_MODELS = [Message]
for model in app_config.get_models():
    if not (model in NOT_REGISTERED_MODELS):
        admin.site.register(model)
