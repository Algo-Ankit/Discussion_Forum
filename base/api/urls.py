from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getroutes),
    path('rooms/', views.getRooms),
    path('rooms/<str:pk>/', views.getRoom),
]