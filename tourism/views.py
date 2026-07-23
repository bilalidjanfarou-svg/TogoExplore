from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required



from .models import TouristSite, Region, Category, Review, Favorite
from .serializers import (
    TouristSiteSerializer,
    RegionSerializer,
    CategorySerializer,
    ReviewSerializer
)


def home(request):
    sites = TouristSite.objects.all()

    context = {
        'sites': sites
    }

    return render(
        request,
        'tourism/index.html',
        context
    )

def site_detail(request, id):

    site = get_object_or_404(
        TouristSite,
        id=id
    )

    reviews = Review.objects.filter(
        site=site
    ).order_by('-created_at')

    if request.method == 'POST':

        name = request.POST.get('name')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            site=site,
            name=name,
            rating=rating,
            comment=comment
        )

        return redirect(
            'site_detail',
            id=site.id
        )

    context = {
        'site': site,
        'reviews': reviews
    }

    return render(
        request,
        'tourism/site_detail.html',
        context
    )


@api_view(['GET'])
def tourist_sites_api(request):

    sites = TouristSite.objects.all()

    search = request.GET.get('search')
    region = request.GET.get('region')
    category = request.GET.get('category')

    # Recherche par nom, description ou localisation
    if search:
        sites = sites.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(location__icontains=search)
        )

    # Filtrer par région
    if region:
        sites = sites.filter(
            region__name__icontains=region
        )

    # Filtrer par catégorie
    if category:
        sites = sites.filter(
            category__name__icontains=category
        )

    serializer = TouristSiteSerializer(
        sites,
        many=True,
        context={'request': request}
    )

    return Response(serializer.data)


@api_view(['GET'])
def tourist_site_detail_api(request, id):

    site = get_object_or_404(
        TouristSite,
        id=id
    )

    serializer = TouristSiteSerializer(
        site,
        context={'request': request}
    )

    return Response(serializer.data)


@api_view(['GET'])
def region_api(request):

    regions = Region.objects.all()

    serializer = RegionSerializer(
        regions,
        many=True
    )

    return Response(serializer.data)


@api_view(['GET'])
def category_api(request):

    categories = Category.objects.all()

    serializer = CategorySerializer(
        categories,
        many=True
    )

    return Response(serializer.data)


@api_view(['GET', 'POST'])
def review_api(request, site_id):

    site = get_object_or_404(
        TouristSite,
        id=site_id
    )

    # Récupérer les avis
    if request.method == 'GET':

        reviews = Review.objects.filter(
            site=site
        ).order_by('-created_at')

        serializer = ReviewSerializer(
            reviews,
            many=True
        )

        return Response(serializer.data)

    # Ajouter un avis
    if request.method == 'POST':

        data = request.data.copy()
        data['site'] = site.id

        serializer = ReviewSerializer(
            data=data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )





@login_required
def add_favorite(request, site_id):

    site = get_object_or_404(
        TouristSite,
        id=site_id
    )

    Favorite.objects.get_or_create(
        user=request.user,
        site=site
    )

    return redirect(
        'site_detail',
        id=site.id
    )

@login_required
def favorites(request):
    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related('site')

    return render(
        request,
        'tourism/favorites.html',
        {'favorites': favorites}
    )

@login_required
def remove_favorite(request, site_id):
    favorite = get_object_or_404(
        Favorite,
        user=request.user,
        site_id=site_id
    )

    favorite.delete()

    return redirect('favorites')


@login_required
def add_favorite(request, site_id):
    site = get_object_or_404(
        TouristSite,
        id=site_id
    )

    Favorite.objects.get_or_create(
        user=request.user,
        site=site
    )

    return redirect('site_detail', id=site.id)


@login_required
def favorites(request):
    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related('site')

    return render(
        request,
        'tourism/favorites.html',
        {
            'favorites': favorites
        }
    )