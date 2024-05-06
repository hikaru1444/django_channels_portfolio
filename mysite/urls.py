# mysite/urls.py
from django.contrib import admin
from django.urls import include, path
from chat.views import index

urlpatterns = [
    path("chat/", include("chat.urls"), name="chat_index"),
    path("admin/", admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path("", index),
]