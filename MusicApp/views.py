from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

from .recommender import search_songs
from .recommender import get_songs
from .serializer import LikedSongsSerializer
from .serializer import UserSerializer
from .models import LikedSongs


def index(request):
    if request.user.is_authenticated:
        return render(request, 'loginindex.html')
    return render(request, 'nologinindex.html')


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def account(request):
    return render(request, 'registration/account.html')


@login_required
def search(request):
    return render(request, 'results.html')


def songs_json(request):
    songlist = [song.spotify_id for song in LikedSongs.objects.filter(user=request.user)]
    return JsonResponse(get_songs(songlist), safe=False)


class SongsList(APIView):
    def get(self, request):
        songs = LikedSongs.objects.filter(user=request.user)
        songs_serializer = LikedSongsSerializer(songs, many=True)
        return Response(songs_serializer.data)

    def post(self, request):
        songs_serializer = LikedSongsSerializer(data=request.data)
        if songs_serializer.is_valid():
            songs_serializer.save()
        return Response(songs_serializer.data)


class UserDetail(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(instance=user)
        return Response(serializer.data)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def search_json(request, query):
    return JsonResponse(search_songs(query), safe=False)


def like(request, song):
    if request.method == "POST":
        try:
            liked = LikedSongs.objects.get(spotify_id=song)
        except LikedSongs.DoesNotExist:
            liked = LikedSongs()
            liked.spotify_id = song
            liked.user = request.user
            liked.save()
        return Response(status=status.HTTP_200_OK)
