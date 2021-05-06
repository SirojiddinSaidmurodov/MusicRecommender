from django.urls import path, include

from MusicApp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/signup', views.signup, name='signup'),
    path('account', views.account, name='account'),
    path('searchhtml', views.searchhtml, name='searchhtml'),
    path('api-auth/', include('rest_framework.urls')),
    path('songsjson/', views.songs_json),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]
