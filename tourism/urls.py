from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Sites
    path(
        'sites/<int:site_id>/',
        views.site_detail,
        name='site_detail'
    ),

    # Contact
    path(
        'contact/',
        views.contact,
        name='contact'
    ),

    # API Sites
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

    # API Régions et catégories
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

    # API Avis
    path(
        'api/sites/<int:site_id>/reviews/',
        views.review_api,
        name='review-api'
    ),

    # Favoris
    path(
        'sites/<int:site_id>/favorite/',
        views.add_favorite,
        name='add_favorite'
    ),

    path(
        'sites/<int:site_id>/remove-favorite/',
        views.remove_favorite,
        name='remove_favorite'
    ),

    path(
        'favorites/',
        views.favorites,
        name='favorites'
    ),

    # Authentification
    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'api/dashboard/',
        views.dashboard_api,
        name='dashboard-api'
    ),

    path(
        'api/sites/top-rated/',
        views.top_rated_sites_api,
        name='top-rated-sites-api'
    )
]