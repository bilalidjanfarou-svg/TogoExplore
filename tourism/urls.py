from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path(
        'api/sites/',
        views.tourist_sites_api,
        name='tourist-sites-api'
    ),
    path(
    'api/sites/<int:id>/',
    views.tourist_site_detail_api,
    name='tourist-site-detail-api'
),
path(
    'api/regions/',
    views.region_api,
    name='regions-api'
),

path(
    'api/categories/',
    views.category_api,
    name='categories-api'
),
]