from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('site/<int:id>/', views.site_detail, name='site_detail'),

    path('contact/', views.contact, name='contact'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
   path(
    'favorite/<int:site_id>/',
    views.add_favorite,
    name='add_favorite'
),




]