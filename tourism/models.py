from django.db import models

# Create your models here.
class TouristSite(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='site/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name