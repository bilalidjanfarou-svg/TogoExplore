from rest_framework import serializers
from .models import TouristSite


class TouristSiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = TouristSite
        fields = '__all__'