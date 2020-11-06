from django.forms import ModelForm


from dal import autocomplete
from django import forms

import datetime

from .models import *

from django.conf import settings

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['code', 'description']

class HMOForm(forms.ModelForm):

    class Meta:
        model = HMO
        fields = ['code', 'description']

class DoctorForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = ['code', 'last_name', 'first_name', 'middle_name', 'specialization', 'contact_number']

class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['last_name', 'first_name', 'middle_name', 'contact_number']

class HMOBillForm(forms.ModelForm):

    # utility_date = forms.DateField(widget=forms.widgets.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}), input_formats=('%d/%m/%Y', ))
    hmo = forms.ModelChoiceField(queryset=HMO.objects.all(), widget=autocomplete.ModelSelect2(url='hmo-autocomplete'))
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), widget=autocomplete.ModelSelect2(url='patient-autocomplete'))
    item = forms.ModelChoiceField(queryset=Item.objects.all(), widget=autocomplete.ModelSelect2(url='item-autocomplete'))
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), widget=autocomplete.ModelSelect2(url='doctor-autocomplete'), required=False)

    class Meta:
        model = HMOBill
        fields = ('__all__')
        exclude = ['user', 'status', 'bill_status']

    def __init__(self, *args, **kwargs):
        super(HMOBillForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control-sm'

class HMOBillUpdateForm(forms.ModelForm):
    
    class Meta:
        model = HMOBill
        fields = '__all__'
        exclude = ['user', 'status',]

class HMOBillListUpdateForm(forms.ModelForm):    

    class Meta:
        model = HMOBill
        fields = '__all__'

class SOAForm(forms.ModelForm):

    class Meta:
        model = SOA
        fields = '__all__'

class HMOBillInForm(forms.ModelForm):

    class Meta:
        model = HMOBill
        fields = ('patient',)
        