from django.shortcuts import render, get_object_or_404
from .models import TouristSite


def home(request):

    query = request.Get.get('q')

    if query:
        sites = TouristeSite.objects.filter(name__icontains=query)
    else:
        sites = TouristeSite.object.all()

    context = {
        'sites': sites
    }

    return render(request, 'tourism/index.html', context)

def site_detail(request, id):
     
     site = get_object_or_404(TouristSite, id=id)

    context = {
        'site': site
    }

    return render(request, 'tourism/site_detail.html', context)

def contact(request):

    return render(request, 'tourism/contact.html')