from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import status, generics
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .models import LikedSongs
from .recommender import get_songs, recommend
from .recommender import search_songs
from .serializer import UserSerializer


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


@login_required
def songs_json(request):
    songlist = [song.spotify_id for song in LikedSongs.objects.filter(user=request.user)]
    return JsonResponse(get_songs(songlist), safe=False)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@login_required
def search_json(request, query):
    results = search_songs(query)
    liked = list(LikedSongs.objects.filter(user=request.user).values_list('spotify_id', flat=True))
    for song in results["tracks"]["items"]:
        song["liked"] = song['id'] in liked
    return JsonResponse(results, safe=False)


@login_required
@api_view(('POST', 'DELETE'))
@renderer_classes((JSONRenderer,))
def songs(request, song):
    if request.method == "POST":
        try:
            liked = LikedSongs.objects.get(spotify_id=song)
        except LikedSongs.DoesNotExist:
            liked = LikedSongs()
            liked.spotify_id = song
            liked.user = request.user
            liked.save()
        return Response(status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        try:
            liked = LikedSongs.objects.get(spotify_id=song)
            liked.delete()
            return Response(status=status.HTTP_200_OK)
        except LikedSongs.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
@login_required
def get_recommendations(request):
    songlist = [song.spotify_id for song in LikedSongs.objects.filter(user=request.user)]
    if len(songlist) > 0:
        return JsonResponse(get_songs(recommend(songlist)), safe=False)
    else:
        return JsonResponse("[]", safe=False)


def about(request):
    return render(request, 'nologinindex.html')
