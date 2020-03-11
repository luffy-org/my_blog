from django.contrib import admin

# Register your models here.
from article import models

for item in models.__all__:
    admin.site.register(getattr(models, item))