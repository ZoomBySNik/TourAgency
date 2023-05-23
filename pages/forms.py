from django import forms
from django.contrib.auth.forms import UserCreationForm
from tours.models import Customer


class CustomerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')
    phone_number = forms.CharField(max_length=18, label='Номер телефона')

    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = UserCreationForm.Meta.fields + ('phone_number','first_name', 'last_name')