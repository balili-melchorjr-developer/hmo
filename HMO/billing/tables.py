import django_tables2 as tables

from .models import HMOBill

class HMOBillTable(tables.Table):

    selection = tables.CheckBoxColumn(accessor='pk')
    

    class Meta:

        model = HMOBill
        template_name = 'django_tables2/bootstrap.html'
        fields = ('selection', 'utility_date', 'approval_number', 'hmo.description', 'patient', 'doctor.last_name', 'bill_status')