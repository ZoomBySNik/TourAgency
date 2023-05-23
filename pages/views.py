from django.shortcuts import render
from tours.models import *

# Create your views here.


def home_view(request, *args, **kwargs):
    print(*args, **kwargs)
    tours = Tour.objects.all()
    news = News.objects.all().order_by('departure_date')
    context = {
        'tours': tours,
        'news': news,
    }
    return render(request, "home.html", context)
