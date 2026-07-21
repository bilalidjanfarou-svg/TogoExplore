from django.contrib import admin
from .models import (
     Region,
    Category,
    TouristSite,
    Gallery,
    Review,
    Contact,
)



@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    liste_display = ("name",)
    search_field = ("name",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    liste_display = ("name",)
    search_field = ("name",)

@admin.register(TouristSite)
class TouristeSiteAdmin(admin.ModelAdmin):
    liste_display = ("name",
                     "location",
                     "region",
                     "categoty",
                     "created_at",
                     )
    liste_filter = ("region",
                    "category",
                    )
    search_field = ("name",
                    "location",
                    "description",
                    )
    
@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    liste_display = ("site",
                     )
    
@admin.register(Review)
class Reviewadmin(admin.ModelAdmin):
    liste_displays = ("name",
                      "site",
                      "rating",
                      "created_at",
                      )
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    liste_display = ("name",
                     "email",
                     "subject",
                     )
