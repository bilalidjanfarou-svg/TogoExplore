from django.shortcuts import render
from .models import TouristSite


def home(request):
    sites = TouristSite.objects.all()

    context = {
        'sites' : sites
    }

    return render(request, 'tourism/index.html')