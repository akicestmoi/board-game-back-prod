from django.urls import path
from .views import *

urlpatterns = [
    path("lobby/<str:username>", LobbyView.as_view()),
    path("<int:pk>", GameView)
]