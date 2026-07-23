from django.urls import path
from . import views


urlpatterns = [
    # Accueil
    path(
        '',
        views.home,
        name='home'
    ),

    # Liste des sites
    path(
        'api/sites/',
        views.tourist_sites_api,
        name='tourist-sites-api'
    ),

    # Détail d'un site
    path(
        'api/sites/<int:id>/',
        views.tourist_site_detail_api,
        name='tourist-site-detail-api'
    ),

    # Liste des régions
    path(
        'api/regions/',
        views.region_api,
        name='regions-api'
    ),

    # Liste des catégories
    path(
        'api/categories/',
        views.category_api,
        name='categories-api'
    ),

    # Avis d'un site
    path(
        'api/sites/<int:site_id>/reviews/',
        views.review_api,
        name='review-api'
    ),
]