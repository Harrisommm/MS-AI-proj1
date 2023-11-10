from django.shortcuts import render




# Create your views here.
def home_main(request):
    return render(request, 'home_main.html')
# ------------------------------------------------


def move_page(request):
    return render(request, 'video_test.html')

