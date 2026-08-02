from rest_framework import serializers
from django.db.models import Avg
from .models import TouristSite, Region, Category, Review


class TouristSiteSerializer(serializers.ModelSerializer):

    region = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = TouristSite
        fields = [
            "id",
            "name",
            "description",
            "location",
            "latitude",
            "longitude",
            "image",
            "region",
            "category",
            "average_rating",
            "reviews_count",
        ]

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(
            Avg("rating")
        )["rating__avg"]

        return round(avg, 1) if avg else 0

    def get_reviews_count(self, obj):
        return obj.reviews.count()


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"