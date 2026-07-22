from rest_framework import serializers
from .models import TouristSite, Region, Category


class TouristSiteSerializer(serializers.ModelSerializer):

    region = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        model = TouristSite
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'