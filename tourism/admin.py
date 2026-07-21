from django.contrib import admin
from .models import (
     Region,
    Category,
    TouristSite,
    Gallery,
    Review,
    Contact,
)



admin.site.register(Region)
admin.site.register(Category)
admin.site.register(TouristSite)
admin.site.register(Gallery)
admin.site.register(Review)
admin.site.register(Contact)
