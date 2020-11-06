from rest_framework import serializers

from billing.models import *


class PatientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Patient
        fields = ['last_name', 'first_name', 'middle_name', 'contact_number']


class ItemSerializer(serializers.ModelSerializer):

    email = serializers.SerializerMethodField('get_username')

    class Meta:
        model = Item
        fields = ['code', 'description', 'email']

    def get_username(self, item):
        email = item.user.email
        return email

class HMOBillSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HMOBill
        fields = ('utility_date', 'approval_number', 'hmo_description', 'patient_fullname', 'bill_status', 'slug')