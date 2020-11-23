from django import forms
from django.contrib.auth.models import User

from .models import Order

class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(label='Ім\'я')
    last_name = forms.CharField(label='Прізвище')
    email = forms.CharField()

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address','postal_code', 'city']
