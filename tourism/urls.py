from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('site/<int:id>/', views.site_detail, name='site_detail'),

    path('contact/', views.contact, name='contact'),
]