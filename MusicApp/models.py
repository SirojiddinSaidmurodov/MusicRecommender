from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class LikedSongs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spotify_id = models.CharField(max_length=22)
