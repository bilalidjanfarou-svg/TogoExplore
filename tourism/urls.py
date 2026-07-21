from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path(
        'api/sites/',
        views.tourist_sites_api,
        name='tourist-sites-api'
    ),
]