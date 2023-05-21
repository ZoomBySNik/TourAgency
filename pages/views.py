from django.shortcuts import render
from tours.models import *

# Create your views here.


def home_view(request, *args, **kwargs):
    print(*args, **kwargs)

    return render(request, "home.html")
