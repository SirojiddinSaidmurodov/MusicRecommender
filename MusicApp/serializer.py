from rest_framework import serializers
from MusicApp import models
from django.contrib.auth.models import User


class LikedSongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LikedSongs
        fields = ('id', 'user', 'spotify_id')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
