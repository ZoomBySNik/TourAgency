from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from tours.models import *


class CustomerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')
    phone_number = forms.CharField(max_length=18, label='Номер телефона')

    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = UserCreationForm.Meta.fields + ('phone_number', 'first_name', 'last_name')


class FilterForTours(forms.Form):
    min_price = forms.IntegerField(label='Цена от', required=False)
    max_price = forms.IntegerField(label='Цена до', required=False)
    min_date = forms.DateField(label='Даты с', required=False)
    max_date = forms.DateField(label='Даты по', required=False)
    type_of_resort = forms.MultipleChoiceField(label='Тип курорта', widget=forms.CheckboxSelectMultiple, required=False)
    departure_city = forms.MultipleChoiceField(label='Город отправления', required=False)
    resort_city = forms.MultipleChoiceField(label='Город назначения', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_of_resort'].choices = [(type_r.id, type_r.title) for type_r in TypeOfResort.objects.all()]
        self.fields['departure_city'].choices = [(city_d.id, city_d.title)
                                                 for city_d in
                                                 City.objects.filter(id__in=Tour.objects.values_list('departure_city'))]
        self.fields['resort_city'].choices = [(city_r.id, city_r.title)
                                              for city_r in
                                              City.objects.filter(hotel__isnull=False).annotate(num_hotels=Count('hotel'))]
