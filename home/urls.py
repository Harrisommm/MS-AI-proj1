# Home app ulrs!

from django.urls import path
from home import views

urlpatterns = [
    path('', views.home_main, name='main'),
    path('video1', views.move_page, name='move_test'),
    
]