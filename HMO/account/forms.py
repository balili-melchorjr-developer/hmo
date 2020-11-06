from django import forms

from django.forms import SelectDateWidget

from django.contrib.auth.forms import UserCreationForm

from .models import Account

from django.utils import timezone


import datetime

def past_years():
    this_year = timezone.now().year
    return list(range(this_year))


class SignUpForm(UserCreationForm):

    hundred_years_from_now = (datetime.datetime.now().year)
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(hundred_years_from_now, 1919, -1)))
    
    class Meta:
        model = Account
        fields = ['email', 'last_name', 'first_name', 'date_of_birth', 'password1', 'password2']



