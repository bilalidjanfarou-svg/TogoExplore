from django.shortcuts import render, get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import TouristSite, Region, Category
from .serializers import (
    TouristSiteSerializer,
    RegionSerializer,
    CategorySerializer
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


@api_view(['GET'])
def tourist_sites_api(request):
    sites = TouristSite.objects.all()

    serializer = TouristSiteSerializer(
        sites,
        many=True
    )

    return Response(serializer.data)


@api_view(['GET'])
def tourist_site_detail_api(request, id):
    site = get_object_or_404(
        TouristSite,
        id=id
    )

    serializer = TouristSiteSerializer(site)

    return Response(serializer.data)

@api_view(['GET'])
def region_api(request):
    region = Region.objects.all()

    serializer = RegionSerializer(
        region,
        many=True
    )

    return Response(serializer.data)

@api_view(['GET'])
def category_api(request):
    category = Category.objects.all()

    serializer = CategorySerializer(
        category,
        many=True
    )

    return Response(serializer.data)