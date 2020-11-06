from django.contrib import admin

from .models import *
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
        list_display = ('code', 'description', 'status')
        search_fields = ('code', 'description')
        readonly_fields = ('status', 'slug', 'user')

        ordering = ('description',)

        filter_horizontal = ()
        list_filter = ()
        fieldsets = ()


class HMOAdmin(admin.ModelAdmin):
        list_display = ('code', 'description', 'status')
        search_fields = ('code', 'description')
        readonly_fields = ('status', 'slug', 'user')

        ordering = ('description',)

        filter_horizontal = ()
        list_filter = ()
        fieldsets = ()

class DoctorAdmin(admin.ModelAdmin):
        list_display = ('last_name', 'first_name', 'specialization', 'status')
        search_fields = ('last_name', 'first_name', 'specialization')
        readonly_fields = ('status', 'slug', 'user')

        ordering = ('last_name',)

        filter_horizontal = ()
        list_filter = ()
        fieldsets = ()

class PatientAdmin(admin.ModelAdmin):
        list_display = ('last_name', 'first_name', 'status')
        search_fields = ('last_name', 'first_name')
        readonly_fields = ('status', 'slug', 'user')

        ordering = ('last_name',)

        filter_horizontal = ()
        list_filter = ()
        fieldsets = ()

class HMOBillAdmin(admin.ModelAdmin):
        list_display = ('utility_date', 'hmo', 'patient', 'bill_status')
        search_fields = ('utility_date', 'hmo', 'patient', 'bill_status')
        readonly_fields = ('status', 'slug', 'user')

        ordering = ('patient',)

        

        filter_horizontal = ()
        list_filter = ()
        fieldsets = ()

class SOAAdmin(admin.ModelAdmin):
        list_display = ('user', 'hmo_bill', 'soa_number')
        search_fields = ('soa_number',)
        readonly_fields = ('soa_number',)

        ordering = ('soa_number',)

        filter_horizontal = ()
        list_filter = ()
        fieldsets = ()

admin.site.register(Item, ItemAdmin)
admin.site.register(HMO, HMOAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(HMOBill, HMOBillAdmin)
admin.site.register(SOA, SOAAdmin)
