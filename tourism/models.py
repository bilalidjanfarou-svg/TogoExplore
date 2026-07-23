from django.db import models
from django.contrib.auth.models import User

class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TouristSite(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="sites",
        null=True,
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="Sites",
        null=True,
        blank=True
    )

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    image = models.ImageField(upload_to="sites/")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    site = models.ForeignKey(
        TouristSite,
        on_delete=models.CASCADE,
        related_name="gallery"
    )

    image = models.ImageField(upload_to="gallery/")

    def __str__(self):
        return f"Image de {self.site.name}"


class Review(models.Model):
    site = models.ForeignKey(
        TouristSite,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.site.name}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    site = models.ForeignKey(
        TouristSite,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'site')

    def __str__(self):
        return f"{self.user.username} - {self.site.name}"