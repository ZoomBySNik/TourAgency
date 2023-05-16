from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Customer(User):
    phone_number = models.CharField(max_length=18, verbose_name='Номер телефона')

    def __str__(self):
        return '%s %s %s' % (self.first_name, self.last_name, self.phone_number)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class TourismManager(User):
    date_of_employment = models.DateField(verbose_name='Дата приема на работу')
    date_of_dismissal = models.DateField(null=True, blank=True, verbose_name='Дата увольнения')

    def __str__(self):
        return '%s %s %s' % (self.first_name, self.last_name, self.date_of_employment)

    class Meta:
        verbose_name = 'Менеджер по туризму'
        verbose_name_plural = 'Менеджеры по туризму'


class TypeOfHotelRoom(models.Model):
    title = models.CharField(null=False, blank=False, max_length=30, unique=True, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return '%s' % (self.title)

    class Meta:
        verbose_name = 'Тип номера'
        verbose_name_plural = 'Типы номеров'


class TypeОfHotelCatering(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return '%s' % (self.title)

    class Meta:
        verbose_name = 'Тип питания'
        verbose_name_plural = 'Типы питаний'


class City(models.Model):
    title = models.CharField(max_length=80, unique=True, verbose_name='Наименование')

    def __str__(self):
        return '%s' % (self.title)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Hotel(models.Model):
    STAR_CHOICES = (
        (0, 'Нет звезд'),
        (1, '1 звезда'),
        (2, '2 звезды'),
        (3, '3 звезды'),
        (4, '4 звезды'),
        (5, '5 звезд'),
    )

    title = models.CharField(max_length=80, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='Город')
    address = models.CharField(max_length=120, verbose_name='Адрес')
    star_rating = models.IntegerField(
        choices=STAR_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name='Звездность гостиницы'
    )

    def __str__(self):
        return '%s %s %s %s звезды' % (self.title, self.city, self.address, self.star_rating)

    class Meta:
        unique_together = ('title', 'city')
        verbose_name = 'Гостиница'
        verbose_name_plural = 'Гостиницы'


class LivingConditions(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT, verbose_name='Отель')
    type_of_hotel_room = models.ForeignKey(TypeOfHotelRoom, on_delete=models.PROTECT, verbose_name='Тип номера')
    type_of_hotel_catering = models.ForeignKey(TypeОfHotelCatering,
                                               on_delete=models.PROTECT, verbose_name='Тип питания')

    def __str__(self):
        return '%s %s %s' % (self.hotel, self.type_of_hotel_room, self.type_of_hotel_catering)

    class Meta:
        verbose_name = 'Условия проживания'
        verbose_name_plural = 'Условия проживания'


class Insurance(models.Model):
    title = models.CharField(max_length=120, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Условия страховки')

    def __str__(self):
        return '%s' % (self.title)

    class Meta:
        verbose_name = 'Страховка'
        verbose_name_plural = 'Страховки'


class TypeOfResort(models.Model):
    title = models.CharField(max_length=120, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return '%s' % (self.title)

    class Meta:
        verbose_name = 'Тип курорта'
        verbose_name_plural = 'Типы курортов'


class AdditionalService(models.Model):
    title = models.CharField(max_length=120, verbose_name='Наименование')
    type_of_service = models.CharField(max_length=40, verbose_name='Вид услуги')

    def __str__(self):
        return '%s %s' % (self.title, self.type_of_service)

    class Meta:
        verbose_name = 'Дополнительная услуга'
        verbose_name_plural = 'Дополнительные услуги'


class Tour(models.Model):
    title = models.CharField(max_length=120, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    departure_city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='Город отправления')
    insurance = models.ForeignKey(Insurance, on_delete=models.PROTECT, verbose_name='Страховка')
    type_of_resort = models.ForeignKey(TypeOfResort, on_delete=models.PROTECT, verbose_name='Тип курорта')
    living_conditions = models.ForeignKey(LivingConditions, on_delete=models.PROTECT, verbose_name='Условия проживания')


    def __str__(self):
        return '%s %s %s' % (self.title, self.type_of_resort, self.living_conditions.hotel.city)

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'



class Service(models.Model):
    tour = models.ForeignKey(Tour, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Тур')
    additional_service = models.ForeignKey(AdditionalService, blank=True, null=True,
                                           on_delete=models.PROTECT, verbose_name='Дополнительная услуга')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    start_date = models.DateField(blank=True, null=True, verbose_name='Дата начала(для туров)')
    end_date = models.DateField(blank=True, null=True, verbose_name='Дата окончания(для туров)')

    def clean(self):
        if self.tour_id and self.additional_service_id:
            raise ValidationError('Можно заполнить только одно из полей Тур или Сервис')

    def __str__(self):
        return '%s' % (self.price)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class BookingRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('processing', 'В обработке'),
        ('approved', 'Подтверждена'),
        ('rejected', 'Отклонена'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name='Клиент')
    date_of_request = models.DateField(auto_now_add=True, editable=False, verbose_name='Дата заявки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус заявки')

    def __str__(self):
        return '%s %s %s %s' % (self.customer.first_name, self.customer.last_name, self.date_of_request, self.status)

    class Meta:
        verbose_name = 'Заявка на бронирование'
        verbose_name_plural = 'Заявки на бронирование'


class BookingRequestPosition(models.Model):
    booking_order = models.ForeignKey(BookingRequest, on_delete=models.PROTECT, verbose_name='Заявка на бронирование')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, verbose_name='Услуга')
    count = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)], verbose_name='Количество')

    def __str__(self):
        return '%s %s %s' % (self.booking_order, self.service, self.count)

    class Meta:
        verbose_name = 'Позиция заявки'
        verbose_name_plural = 'Позиции заявок'