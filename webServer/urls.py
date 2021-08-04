from django.urls import path
from .views import Home, Download, Download1, About

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('download', Download.as_view(), name='download'),
    path('download1', Download1.as_view(), name='download1'),
    path('about', About.as_view(), name='about'),
]
