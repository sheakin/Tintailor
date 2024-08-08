from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('index',IndexView.as_view(),name="index"),

    path("log",LoginView.as_view(),name="log"),
    path("reg",RegView.as_view(),name="reg"),
    path('logout', LogoutView.as_view(), name="logout"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


