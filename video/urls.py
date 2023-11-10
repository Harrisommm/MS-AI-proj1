from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('video_page1', views.video1, name='video1'),
    path('video_page2', views.video2, name='video2'),
]