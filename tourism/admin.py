from django.contrib import admin
from .models import TouristSite, Category



# Register your models here. 
admin.site.register(Category)
admin.site.register(TouristSite)
