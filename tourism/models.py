from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
class TouristSite(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='site/')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    authors = models.CharField(max_length=100)
    site = models.ForeignKey(
        TouristSite,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    author = models.CharField(max_length=100)

    comment = models.TextField()

    rating = models.IntegerField(default=5)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.site.name}"

class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    site = models.ForeignKey(
        TouristSite,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user', 'site')

















