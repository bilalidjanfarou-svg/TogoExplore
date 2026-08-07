from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.paginator import Paginator

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

    sites = TouristSite.objects.all().order_by("-created_at")

    categories = Category.objects.all()
    regions = Region.objects.all()

    q = request.GET.get("q")

    if q:
        sites = sites.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(location__icontains=q)
        )

    category = request.GET.get("category")

    if category:
        sites = sites.filter(category_id=category)

    region = request.GET.get("region")

    if region:
        sites = sites.filter(region_id=region)

    sort = request.GET.get("sort")

    if sort == "name":
        sites = sites.order_by("name")

    elif sort == "recent":
        sites = sites.order_by("-created_at")

    paginator = Paginator(sites, 6)

    page = request.GET.get("page")

    sites = paginator.get_page(page)

    return render(
        request,
        "tourism/index.html",
        {
            "sites": sites,
            "categories": categories,
            "regions": regions,
        }
    )



# ==========================================================
# DÉTAIL D'UN SITE TOURISTIQUE
# ==========================================================

def site_detail(request, site_id):

    site = get_object_or_404(
        TouristSite,
        id=site_id
    )

    reviews = site.reviews.order_by("-created_at")

    if request.method == "POST":

        Review.objects.create(
            site=site,
            name=request.POST.get("name"),
            rating=request.POST.get("rating"),
            comment=request.POST.get("comment")
        )

        return redirect(
            "site_detail",
            site_id=site.id
        )

    return render(
        request,
        "tourism/site_detail.html",
        {
            "site": site,
            "reviews": reviews,
        }
    )


# ==========================================================
# CONTACT
# ==========================================================

def contact(request):

    if request.method == "POST":

        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message"),
        )

        return redirect("contact")

    return render(
        request,
        "tourism/contact.html",
    )


# ==========================================================
# API - LISTE DES SITES
# ==========================================================

@api_view(["GET"])
def tourist_sites_api(request):

    sites = TouristSite.objects.all()

    search = request.GET.get("search")
    region = request.GET.get("region")
    category = request.GET.get("category")

    if search:
        sites = sites.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(location__icontains=search)
        )

    if region:
        sites = sites.filter(
            region__name__icontains=region
        )

    if category:
        sites = sites.filter(
            category__name__icontains=category
        )

    serializer = TouristSiteSerializer(
        sites,
        many=True,
        context={"request": request}
    )

    return Response(serializer.data)


# ==========================================================
# API - DÉTAIL D'UN SITE
# ==========================================================

@api_view(["GET"])
def tourist_site_detail_api(request, id):

    site = get_object_or_404(
        TouristSite,
        id=id
    )

    serializer = TouristSiteSerializer(
        site,
        context={"request": request}
    )

    return Response(serializer.data)


# ==========================================================
# API - RÉGIONS
# ==========================================================

@api_view(["GET"])
def region_api(request):

    serializer = RegionSerializer(
        Region.objects.all(),
        many=True
    )

    return Response(serializer.data)

# ==========================================================
# API - CATÉGORIES
# ==========================================================

@api_view(["GET"])
def category_api(request):

    serializer = CategorySerializer(
        Category.objects.all(),
        many=True
    )

    return Response(serializer.data)


# ==========================================================
# API - AVIS
# ==========================================================


@api_view(["GET", "POST"])
def review_api(request, site_id):

    site = get_object_or_404(
        TouristSite,
        id=site_id
    )

    if request.method == "GET":

        serializer = ReviewSerializer(
            site.reviews.all().order_by("-created_at"),
            many=True
        )

        return Response(serializer.data)

    serializer = ReviewSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save(site=site)

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
        "site_detail",
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
        "site_detail",
        site_id=site.id
    )


# ==========================================================
# FAVORIS - LISTE
# ==========================================================

@login_required
def favorites(request):

    favorite_sites = Favorite.objects.filter(
        user=request.user
    ).select_related("site")

    return render(
        request,
        "tourism/favorites.html",
        {
            "favorite_sites": favorite_sites
        }
    )


# ==========================================================
# INSCRIPTION
# ==========================================================
def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:

            return render(
                request,
                "registration/register.html",
                {
                    "error": "Les mots de passe ne correspondent pas."
                }
            )

        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                "registration/register.html",
                {
                    "error": "Ce nom d'utilisateur existe déjà."
                }
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(
            request,
            user
        )

        return redirect("home")

    return render(
        request,
        "registration/register.html"
    )
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_api(request):

    return Response({

        "username": request.user.username,

        "email": request.user.email,

        "favorites": Favorite.objects.filter(
            user=request.user
        ).count(),

        "reviews": Review.objects.filter(
            name=request.user.username
        ).count(),

        "sites": TouristSite.objects.count()

    })
@api_view(["GET"])
def top_rated_sites_api(request):

    sites = TouristSite.objects.annotate(
        avg_rating=Avg("reviews__rating")
    ).order_by("-avg_rating")[:5]

    serializer = TouristSiteSerializer(
        sites,
        many=True,
        context={"request": request}
    )

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_favorites_api(request):

    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related("site")

    serializer = TouristSiteSerializer(
        [favorite.site for favorite in favorites],
        many=True,
        context={"request": request}
    )

    return Response(serializer.data)

@api_view(["GET", "POST"])
def review_api(request, site_id):

    site = get_object_or_404(
        TouristSite,
        id=site_id
    )

    if request.method == "GET":
        reviews = Review.objects.filter(
            site=site
        ).order_by("-created_at")

        serializer = ReviewSerializer(
            reviews,
            many=True
        )

        return Response(serializer.data)

    serializer = ReviewSerializer(
        data=request.data
    )

    if serializer.is_valid():
        serializer.save(site=site)
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)