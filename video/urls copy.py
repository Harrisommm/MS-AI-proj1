from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('video_page1', views.video, name='video1'),
]