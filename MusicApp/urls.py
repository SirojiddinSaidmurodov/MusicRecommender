from django.urls import path, include

from MusicApp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/signup', views.signup, name='signup'),
    path('account', views.account, name='account'),
    path('search/', views.search, name='search'),
    path('search/<str:query>', views.search_json),
    path('api-auth/', include('rest_framework.urls')),
    path('songsjson/', views.songs_json)
]
