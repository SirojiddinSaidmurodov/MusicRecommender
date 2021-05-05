from django.urls import path

from MusicApp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/signup', views.signup, name='signup'),
    path('account', views.account, name='account'),
]
