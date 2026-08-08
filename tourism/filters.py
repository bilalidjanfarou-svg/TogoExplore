import django_filters

from .models import TouristSite


class TouristSiteFilter(django_filters.FilterSet):

    class Meta:
        model = TouristSite

        fields = [
            "region",
            "category",
        ]