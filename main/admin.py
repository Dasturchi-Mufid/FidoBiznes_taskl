from django.contrib import admin
from django.apps import apps

# Get the list of all models in the current app
app_models = apps.get_models()

for model in app_models:
    try:
        # Register the model with the default ModelAdmin
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        # If the model is already registered, ignore it
        pass
