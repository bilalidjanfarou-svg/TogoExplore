from django.contrib import admin
from .models import TouristSite, Category, Review




admin.site.register(Category)
admin.site.register(TouristSite)
admin.site.register(Review)
