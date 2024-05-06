# chat/urls.py
from django.urls import path
from . import views
from chat.models import Shop


urlpatterns = [
    path("", views.index, name="index"),
    path("room/", views.RoomView.as_view(model=Shop), name="room"),
]
