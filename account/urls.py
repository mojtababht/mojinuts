from django.urls import path
from .views import *

urlpatterns = [
    path('signup/',SignUpView.as_view(),name='signup'),
    path('logedin/',LogedInView.as_view(),name='logedin'),
    path('profile/<int:pk>/',ProfileView.as_view(),name='profile'),
    path('profile/edit/<int:pk>',ProfileUpdateView.as_view(),name='profileupdate'),

]