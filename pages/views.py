from sqlite3 import Date

from django.http import Http404

from tours.models import *
from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm, FilterForTours
from decimal import Decimal


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
    news = News.objects.all().order_by('-departure_date')
    context = {
        'tours': tours,
        'news': news,
    }
    user = request.user.id
    return render(request, "home.html", context)


def news_view(request):
    news = News.objects.order_by('-departure_date').all()
    context = {
        'news':news
    }
    return render(request, "news.html", context)


def tours_view(request):
    tours = Service.objects.filter(tour__isnull=False)
    form = FilterForTours(request.GET)
    if form.is_valid():
        if form.cleaned_data["min_price"]:
            min_price = Decimal(form.cleaned_data["min_price"])
            tours = tours.filter(price__gte=min_price)
        if form.cleaned_data["max_price"]:
            max_price = Decimal(form.cleaned_data["max_price"])
            tours = tours.filter(price__lte=max_price)
        if form.cleaned_data["min_date"]:
            min_date = form.cleaned_data["min_date"]
            tours = tours.filter(start_date__gte=min_date)
        if form.cleaned_data["max_date"]:
            max_date = form.cleaned_data["max_date"]
            tours = tours.filter(end_date__lte=max_date)
        if 'reset' in request.GET:
            return redirect('tours_view')

    context = {
        'tours': tours,
        'form': form,
    }
    return render(request, "tours.html", context)


def tour_detail(request, id):
    try:
        service = Service.objects.get(id=id)
        context = {'service': service}
        return render(request, 'tour.html', context)
    except Service.DoesNotExist:
        raise Http404("Service does not exist")


def create_request_on_tour(request, id):
    customer = Customer.objects.get(id=request.user.id)
    book_request = BookingRequest(customer=customer)
    book_request.save()

    book_request_position = BookingRequestPosition(count=1, booking_order=book_request, service_id=id)
    book_request_position.save()

    private_message = PrivateMessage(sender_person=request.user,
                                     recipient_person=User.objects.get(first_name='System'),
                                     content='Ваша заявка на бронирование успешно создана\n'+str(Service.objects.get(id=id)))
    private_message.save()
    return redirect('news')