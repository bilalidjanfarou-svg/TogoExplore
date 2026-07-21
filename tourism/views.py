from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import TouristSite
from .serializers import TouristSiteSerializer


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