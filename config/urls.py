from django.urls import path, include

# Import your custom admin site
from apps.core.admin import vector_lmd_admin
from django.apps import apps

# Auto-register your models with the custom admin site
# This ensures all your models are registered with the new admin site
for app_config in apps.get_app_configs():
    for model in app_config.get_models():
        try:
            vector_lmd_admin.register(model)
        except admin.sites.AlreadyRegistered:
            pass

urlpatterns = [
    # Use your custom admin site instead of the default
    path("admin/", vector_lmd_admin.urls),
    # ...existing code...
]
