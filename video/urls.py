# Video app ulrs!

from django.urls import path
from video import views

urlpatterns = [
    path('video_test', views.video, name='video_output'),
]