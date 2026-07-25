from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import (
    TouristSite,
    Region,
    Category,
    Review,
    Favorite,
    Contact
)

from .serializers import (
    TouristSiteSerializer,
    RegionSerializer,
    CategorySerializer,
    ReviewSerializer
)


# ==========================================================
# ACCUEIL
# ==========================================================

def home(request):
    sites = TouristSite.objects.all()
    categories = Category.objects.all()
    regions = Region.objects.all()

    # Recherche
    q = request.GET.get('q')

    if q:
        sites = sites.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(location__icontains=q)
        )

    # Filtre par catégorie
    category_id = request.GET.get('category')

    if category_id:
        sites = sites.filter(
            category_id=category_id
        )

    # Filtre par région
    region_id = request.GET.get('region')

    if region_id:
        sites = sites.filter(
            region_id=region_id
        )

    context = {
        'sites': sites,
        'categories': categories,
        'regions': regions,
    }

    return render(
        request,
        'tourism/index.html',
        context
    )


# ==========================================================
# DÉTAIL D'UN SITE TOURISTIQUE
# ==========================================================

def site_detail(request, site_id):

    site = get_object_or_404(
        TouristSite,
        id=site_id
    )

    reviews = Review.objects.filter(
        site=site
    ).order_by('-created_at')

    # Ajouter un avis depuis le site web
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
            site_id=site.id
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


# ==========================================================
# CONTACT
# ==========================================================

def contact(request):

    if request.method == 'POST':

        Contact.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )

        return redirect('contact')

    return render(
        request,
        'tourism/contact.html'
    )


# ==========================================================
# API - LISTE DES SITES
# ==========================================================

@api_view(['GET'])
def tourist_sites_api(request):

    sites = TouristSite.objects.all()

    search = request.GET.get('search')
    region = request.GET.get('region')
    category = request.GET.get('category')

    # Recherche
    if search:
        sites = sites.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(location__icontains=search)
        )

    # Région
    if region:
        sites = sites.filter(
            region__name__icontains=region
        )

    # Catégorie
    if category:
        sites = sites.filter(
            category__name__icontains=category
        )

    serializer = TouristSiteSerializer(
        sites,
        many=True,
        context={'request': request}
    )

    return Response(
        serializer.data
    )


# ==========================================================
# API - DÉTAIL D'UN SITE
# ==========================================================

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

    return Response(
        serializer.data
    )


# ==========================================================
# API - RÉGIONS
# ==========================================================

@api_view(['GET'])
def region_api(request):

    regions = Region.objects.all()

    serializer = RegionSerializer(
        regions,
        many=True
    )

    return Response(
        serializer.data
    )


# ==========================================================
# API - CATÉGORIES
# ==========================================================

@api_view(['GET'])
def category_api(request):

    categories = Category.objects.all()

    serializer = CategorySerializer(
        categories,
        many=True
    )

    return Response(
        serializer.data
    )


# ==========================================================
# API - AVIS
# ==========================================================

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

        return Response(
            serializer.data
        )

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


# ==========================================================
# FAVORIS - AJOUTER
# ==========================================================

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
        site_id=site.id
    )


# ==========================================================
# FAVORIS - SUPPRIMER
# ==========================================================

@login_required
def remove_favorite(request, site_id):

    site = get_object_or_404(
        TouristSite,
        id=site_id
    )

    Favorite.objects.filter(
        user=request.user,
        site=site
    ).delete()

    return redirect(
        'site_detail',
        site_id=site.id
    )


# ==========================================================
# FAVORIS - LISTE
# ==========================================================

@login_required
def favorites(request):

    favorite_sites = Favorite.objects.filter(
        user=request.user
    ).select_related(
        'site'
    )

    return render(
        request,
        'tourism/favorites.html',
        {
            'favorite_sites': favorite_sites
        }
    )


# ==========================================================
# INSCRIPTION
# ==========================================================

def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Vérifier les mots de passe
        if password != password2:

            return render(
                request,
                'registration/register.html',
                {
                    'error':
                    'Les mots de passe ne correspondent pas.'
                }
            )

        # Vérifier si l'utilisateur existe
        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                'registration/register.html',
                {
                    'error':
                    'Ce nom d\'utilisateur existe déjà.'
                }
            )

        # Créer l'utilisateur
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Connecter automatiquement
        login(
            request,
            user
        )

        return redirect(
            'home'
        )

    return render(
        request,
        'registration/register.html'
    )