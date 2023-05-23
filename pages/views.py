from tours.models import *
from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm


def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Перенаправление на главную страницу после успешной регистрации
    else:
        form = CustomerRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})



def home_view(request, *args, **kwargs):
    print(*args, **kwargs)
    tours = Tour.objects.all()
    news = News.objects.all().order_by('departure_date')
    context = {
        'tours': tours,
        'news': news,
    }
    return render(request, "home.html", context)

def news_view(request):
    news = News.objects.order_by('departure_date').all()
    context = {
        'news':news
    }
    return render(request, "news.html", context)