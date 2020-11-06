import django_filters
from django_filters import DateFilter, ModelChoiceFilter, CharFilter

from django import forms

from dal import autocomplete

from django.conf import settings

from .models import *

class HMOBillFilter(django_filters.FilterSet):

    hmo = ModelChoiceFilter(queryset=HMO.objects.all(), widget=autocomplete.ModelSelect2(url='hmo-autocomplete'))
    patient = ModelChoiceFilter(queryset=Patient.objects.all(), widget=autocomplete.ModelSelect2(url='patient-autocomplete'))

    start_date = DateFilter(field_name="utility_date", lookup_expr='gte', label='Start Date')
    end_date = DateFilter(field_name="utility_date", lookup_expr='lte', label='End Date')

    class Meta:
        model = HMOBill
        fields = ('hmo', 'patient')