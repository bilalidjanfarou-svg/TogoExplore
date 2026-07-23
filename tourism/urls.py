from django.urls import path
from . import views


urlpatterns = [
    # Page d'accueil
    path(
        '',
        views.home,
        name='home'
    ),

    # API : liste des sites touristiques
    path(
        'api/sites/',
        views.tourist_sites_api,
        name='tourist-sites-api'
    ),

    # API : détail d'un site touristique
    path(
        'api/sites/<int:id>/',
        views.tourist_site_detail_api,
        name='tourist-site-detail-api'
    ),

    # API : liste des régions
    path(
        'api/regions/',
        views.region_api,
        name='regions-api'
    ),

    # API : liste des catégories
    path(
        'api/categories/',
        views.category_api,
        name='categories-api'
    ),
]