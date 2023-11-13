from django.contrib import admin
from .models import Organization, Certificate

admin.site.register(Organization)
admin.site.register(Certificate)