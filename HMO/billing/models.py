from django.db import models
from dateutil.relativedelta import relativedelta

from datetime import datetime, timedelta, date
import datetime

import uuid

from .tasks import type_hello
 
from django.utils.text import slugify
from decimal import Decimal
from django.db.models import F, Sum
from django.db.models.functions import Abs

from .slugs import unique_slugify, unique_case_id
# Create your models here.
from django.core.validators import RegexValidator, MinValueValidator

from account.models import Account

class Item(models.Model):
    user = models.ForeignKey(Account, default=1, null=True, blank=True, on_delete=models.SET_NULL) 
    code = models.PositiveSmallIntegerField(unique=True)
    description = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, editable=False, default='')
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def get_absolute_url(self):
        return f"/item/{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"
    
    def save(self, **kwargs):
        slug_str = "%s %s" % (self.code, self.description) 
        unique_slugify(self, slug_str)
        super(Item, self).save(**kwargs)

    def __str__(self):
        return '%s - %s' % (self.code, self.description)


class HMO(models.Model):
    user = models.ForeignKey(Account, default=1, null=True, blank=True,  on_delete=models.SET_NULL)
    code = models.PositiveSmallIntegerField(unique=True)
    description = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, editable=False, default='')
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'HMO'
        verbose_name_plural = 'HMOs'

    def get_absolute_url(self):
        return f"/hmo/{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"
    
    def save(self, **kwargs):
        slug_str = "%s %s" % (self.code, self.description) 
        unique_slugify(self, slug_str)
        super(HMO, self).save(**kwargs)

    def __str__(self):
        return '%s - %s' % (self.code, self.description)

class Doctor(models.Model):
    user = models.ForeignKey(Account, default=1, null=True, blank=True,  on_delete=models.SET_NULL)
    code = models.PositiveSmallIntegerField(unique=True)
    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    specialization = models.CharField(max_length=200, null=True, blank=True)
    contact_number = models.CharField(null=True, blank=True, verbose_name='Contact Number', max_length=15, validators=[RegexValidator(r'^\d{0,15}$')])
    slug = models.SlugField(unique=True, max_length=200, editable=False, default='')
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'    


    def get_absolute_url(self):
        return f"/doctor/{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"
    
    def save(self, **kwargs):
        slug_str = "%s %s %s %s" % (self.code, self.specialization, self.last_name, self.first_name ) 
        unique_slugify(self, slug_str)
        super(Doctor, self).save(**kwargs)

    def __str__(self):
        return '%s - %s, %s' % (self.code, self.last_name, self.first_name)


class Patient(models.Model):
    user = models.ForeignKey(Account, default=1, null=True, blank=True,  on_delete=models.SET_NULL)
    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    contact_number = models.CharField(null=True, blank=True, verbose_name='Contact Number', max_length=15, validators=[RegexValidator(r'^\d{0,15}$')])
    slug = models.SlugField(unique=True, max_length=200, editable=False, default='')
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def get_absolute_url(self):
        return f"/patient/{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"
    
    def save(self, **kwargs):
        slug_str = "%s %s" % (self.last_name, self.first_name) 
        unique_slugify(self, slug_str)
        super(Patient, self).save(**kwargs)

    def __str__(self):
        return '%s, %s' % ( self.last_name, self.first_name)

class HMOBill(models.Model):

    STATUS = (
        ('Encoded', 'Encoded'),
        ('Pending', 'Pending'),
        ('Billed', 'Billed'),
    )

    user = models.ForeignKey(Account, default=1, null=True, blank=True,  on_delete=models.SET_NULL) 
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    utility_date = models.DateField(default=datetime.date.today)
    approval_number = models.CharField(max_length=200)
    hmo = models.ForeignKey(HMO, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    charges = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12, validators=[MinValueValidator(0.00)], default=Decimal(0.00))
    professional_fee = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12, validators=[MinValueValidator(0.00)], default=Decimal(0.00))
    doctor = models.ForeignKey(Doctor, null=True, blank=True, on_delete=models.CASCADE)
    credit = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12, validators=[MinValueValidator(0.00)], default=Decimal(0.00))
    total = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12, validators=[MinValueValidator(0.00)], default=Decimal(0.00))
    slug = models.SlugField(unique=True, max_length=200, editable=False, default='')
    bill_status = models.CharField(max_length=200, null=True, choices=STATUS, default='Encoded')
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'HMO Bill'
        verbose_name_plural = 'HMO Bills'  

    def get_absolute_url(self):
        return f"/hmobill/{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"    
    
    def save(self, **kwargs):
        slug_str = "%s %s %s %s" % (self.utility_date, self.approval_number, self.hmo, self.patient)
        total = self.credit - self.charges - self.professional_fee
        self.total = abs(total)
        unique_slugify(self, slug_str)
        super(HMOBill, self).save(**kwargs)

    def __str__(self):
        return '%s' % ( self.patient)

    def hmo_description(self):
        return self.hmo.description

    def patient_fullname(self):
        return self.patient.last_name, self.patient.first_name


from django.db import connection

def IncrementSOANumber():
    last_soa_number = SOA.objects.all().order_by('id').last()

    new_soa_something = SOA.objects.all().order_by('id')
    
    same = 'SOA' + '-'+ str(datetime.date.today().year) + '-' + str(datetime.date.today().month).zfill(2)

    # if not last_soa_number:
    #     return same + '-' + '00001'

    # else:
    #     soa_number = last_soa_number.soa_number
    #     soa_number_int = int(soa_number[12:20])
    #     new_soa_number_int = soa_number_int + 1
    #     new_soa_number = same +'-'+ str(new_soa_number_int).zfill(5)

    conn = connection.cursor()
    #     return new_soa_number
    #  
    
    new_same = '%' + same + '%'
    shellraw = SOA.objects.raw('SELECT soa_number FROM billing_soa WHERE soa_number LIKE %s GROUP BY soa_number', [new_same])
    conn_new = conn.execute('SELECT soa_number FROM billing_soa WHERE soa_number LIKE %s GROUP BY soa_number', [new_same])
    print(shellraw)
    print(conn_new)

    today = date.today()
    first_day = today.replace(day=1) + relativedelta(months=1)

    if not last_soa_number:
        return same + '-' + '00001'

    elif today == date(today.year, today.month, day=1):

        
        if last_soa_number.soa_number == same +'-'+ '00001' or conn_new > 0:
            
            soa_number = last_soa_number.soa_number
            soa_number_int = conn_new
            new_counter = soa_number_int + 1
            new_soa_number = same + '-' + str(new_counter).zfill(5)
            
            return new_soa_number
            
        else:
            return same + '-' + '00001'

    else:
        soa_number = last_soa_number.soa_number
        soa_number_int = conn_new
        new_counter = soa_number_int + 1
        new_soa_number = same + '-' + str(new_counter).zfill(5)
        return new_soa_number

class SOA(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, default=1)
    soa_number = models.CharField(max_length=20, default=IncrementSOANumber, editable=False)
    hmo_bill = models.ForeignKey(HMOBill, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, editable=False, default='')
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'SOA'
        verbose_name_plural = 'SOAs'

    # def get_hmo_bill(self):
    #     return "\n".join([p.hmo_bills for p in self.hmo_bill.all()])

    def get_absolute_url(self):
        return f"/soa/{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"  
    
    def save(self, **kwargs):
        slug_str = "%s" % (self.soa_number)
        unique_slugify(self, slug_str)
        super(SOA, self).save(**kwargs)

    def __str__(self):
        return '%s' % ( self.soa_number)





