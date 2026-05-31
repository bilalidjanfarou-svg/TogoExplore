from django.shortcuts import render, get_object_or_404
from .models import TouristSite, Category


def home(request):

    query = request.GET.get('q')
    category_id = request.GET.get('category')

    sites = TouristSite.objects.all()

    if query:
        sites = sites.filter(name__icontains=query)

    if category_id:
        sites = sites.filter(category_id=category_id)

    categories = Category.objects.all()

    context = {
        'sites': sites,
        'categories': categories
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