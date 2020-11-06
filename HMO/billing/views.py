from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core import serializers

from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import F, Sum, Count, Q
# Create your views here.

from dal import autocomplete

from .filters import HMOBillFilter

from django.forms import inlineformset_factory

from account.decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
from .tables import *

'''----------------------------- Automcomplete --------------------------------'''

class HMOAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #     return Address.objects.none()


        qs = HMO.objects.all().order_by('description')

        if self.q:
            qs = qs.filter(Q(description__icontains=self.q)|Q(code__icontains=self.q))
        return qs

class PatientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #     return Address.objects.none()

        qs = Patient.objects.all().order_by('last_name')

        if self.q:
            qs = qs.filter(Q(last_name__icontains=self.q)|Q(first_name__icontains=self.q))
        return qs

class ItemAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #     return Address.objects.none()

        qs = Item.objects.all().order_by('description')

        if self.q:
            qs = qs.filter(Q(description__icontains=self.q)|Q(code__icontains=self.q))
        return qs

class DoctorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #     return Address.objects.none()

        qs = Doctor.objects.all().order_by('last_name')

        if self.q:
            qs = qs.filter(Q(last_name__icontains=self.q)|Q(first_name__icontains=self.q)|Q(code__icontains=self.q))
        return qs

def home(request):
    hmo_bill = HMOBill.objects.all().order_by('-date_created')

    hmo_bill_total_entry = hmo_bill.count()
    hmo_bill_encoded = hmo_bill.filter(bill_status='Encoded').count()
    hmo_bill_pending = hmo_bill.filter(bill_status='Pending').count()
    hmo_bill_billed = hmo_bill.filter(bill_status='Billed').count()


    template_name = 'home.html'
    context = {'hmo_bill_total_entry': hmo_bill_total_entry,
                'hmo_bill_encoded':hmo_bill_encoded,
                'hmo_bill_pending': hmo_bill_pending,
                'hmo_bill_billed': hmo_bill_billed,
                'hmo_bill': hmo_bill,
                }
    return render(request, template_name, context)


''' -------------------------- Item Section ---------------------------------'''

@login_required(login_url='signin')
def ItemList(request):
    items = Item.objects.all()

    context = {'items': items}
    template_name = 'settings/items/list.html'
    return render(request, template_name, context)

@login_required(login_url='signin')
def ItemDetail(request, slug):

    item_detail = Item.objects.get(slug=slug)

    context = {'item': item_detail}
    template_name = 'settings/items/detail.html'
    return render(request, template_name, context)

@login_required(login_url='signin')
def CreateItem(request):
    form = ItemForm(request.POST or None)

    if form.is_valid():
        obj = form.save(commit=False)
        # obj.title = form.cleaned_data.get('title') + "0" can manipulat pre existing data
        obj.user = request.user
        obj.save()
        form = ItemForm()
        return redirect('item-list')
        
        # title = form.cleaned_data['title']    
        # obj = BlogPost.objects.create(title=title)  you can create and save this column data in multiple models
    template_name = 'settings/items/create.html'
    context = {"form": form}
    return render(request, template_name, context)

@login_required(login_url='signin')
def UpdateItem(request, slug):
    item = Item.objects.get(slug=slug)
    form = ItemForm(request.POST or None, instance=item) # To locate specific date instance=obj
    if form.is_valid():
            form.save()
            return redirect('item-list')            
    template_name = 'settings/items/update.html'
    context = {"form": form, "title": f"Update {item.code}, {item.description}"  }
    return render(request, template_name, context)

@login_required(login_url='signin')
def DeleteItem(request, slug):
    item = Item.objects.get(slug=slug)
    template_name = 'settings/items/delete.html'
    if request.method == "POST":
        item.delete()
        return redirect('item-list')
    context = {"item": item}
    return render(request, template_name, context)

''' -------------------------- HMO Section ---------------------------------'''  

@login_required(login_url='signin')
def HMOList(request):
    hmos = HMO.objects.all()

    context = {'hmos': hmos}
    template_name = 'settings/hmos/list.html'
    return render(request, template_name, context)

@login_required(login_url='signin')
def HMODetail(request, slug):

    hmo_detail = HMO.objects.get(slug=slug)

    context = {'hmo': hmo_detail}
    template_name = 'settings/hmos/detail.html'
    return render(request, template_name, context)

@login_required(login_url='signin')
def CreateHMO(request):
    form = HMOForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # obj.title = form.cleaned_data.get('title') + "0" can manipulat pre existing data
        obj.user = request.user
        obj.save()
        form = HMOForm()
        return redirect('hmo-list')
        
        # title = form.cleaned_data['title']    
        # obj = BlogPost.objects.create(title=title)  you can create and save this column data in multiple models
    template_name = 'settings/hmos/create.html'
    context = {"form": form}
    return render(request, template_name, context)

@login_required(login_url='signin')
def UpdateHMO(request, slug):
    hmo = HMO.objects.get(slug=slug)
    form = HMOForm(request.POST or None, instance=hmo) # To locate specific date instance=obj
    if form.is_valid():
            form.save()
            return redirect('hmo-list')            
    template_name = 'settings/hmos/update.html'
    context = {"form": form, "title": f"Update {hmo.code}, {hmo.description}"  }
    return render(request, template_name, context)

@login_required(login_url='signin')
def DeleteHMO(request, slug):
    hmo = HMO.objects.get(slug=slug)
    template_name = 'settings/hmos/delete.html'
    if request.method == "POST":
        hmo.delete()
        return redirect('hmo-list')
    context = {"hmo": hmo}
    return render(request, template_name, context)

''' -------------------------- Doctor Section ---------------------------------'''  

@login_required(login_url='signin')
def DoctorList(request):
    doctors = Doctor.objects.all()

    context = {'doctors': doctors}
    template_name = 'settings/doctors/list.html'
    return render(request, template_name, context)

@login_required(login_url='signin')
def DoctorDetail(request, slug):

    doctor_detail = Doctor.objects.get(slug=slug)

    context = {'doctor': doctor_detail}
    template_name = 'settings/doctors/detail.html'
    return render(request, template_name, context)

@login_required(login_url='signin')
def CreateDoctor(request):
    form = DoctorForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # obj.title = form.cleaned_data.get('title') + "0" can manipulat pre existing data
        obj.user = request.user
        obj.save()
        form = DoctorForm()
        return redirect('doctor-list')
        
        # title = form.cleaned_data['title']    
        # obj = BlogPost.objects.create(title=title)  you can create and save this column data in multiple models
    template_name = 'settings/doctors/create.html'
    context = {"form": form}
    return render(request, template_name, context)

@login_required(login_url='signin')
def UpdateDoctor(request, slug):
    doctor = Doctor.objects.get(slug=slug)
    form = DoctorForm(request.POST or None, instance=doctor) # To locate specific date instance=obj
    if form.is_valid():
            form.save()
            return redirect('doctor-list')            
    template_name = 'settings/doctors/update.html'
    context = {"form": form, "title": f"Update {doctor.code}, - {doctor.last_name}, {doctor.first_name} -- {doctor.specialization}"  }
    return render(request, template_name, context)

@login_required(login_url='signin')
def DeleteDoctor(request, slug):
    doctor = Doctor.objects.get(slug=slug)
    template_name = 'settings/doctors/delete.html'
    if request.method == "POST":
        doctor.delete()
        return redirect('doctor-list')
    context = {"doctor": doctor}
    return render(request, template_name, context)

''' -------------------------- Patient Section ---------------------------------'''  

@login_required(login_url='signin')
def PatientList(request):
    patients = Patient.objects.all()

    context = {'patients': patients}
    template_name = 'settings/patients/list.html'
    return render(request, template_name, context)

@login_required(login_url='signin')
def PatientDetail(request, slug):

    patient_detail = Patient.objects.get(slug=slug)

    context = {'patient': patient_detail}
    template_name = 'settings/patients/detail.html'
    return render(request, template_name, context)

@login_required(login_url='signin')
def CreatePatient(request):
    form = PatientForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # obj.title = form.cleaned_data.get('title') + "0" can manipulat pre existing data
        obj.user = request.user
        obj.save()
        form = PatientForm()
        return redirect('patient-list')
        
        # title = form.cleaned_data['title']    
        # obj = BlogPost.objects.create(title=title)  you can create and save this column data in multiple models
    template_name = 'settings/patients/create.html'
    context = {"form": form}
    return render(request, template_name, context)

@login_required(login_url='signin')
def CreatePatientModal(request):
    data = dict()
    form = PatientForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # obj.title = form.cleaned_data.get('title') + "0" can manipulat pre existing data
        obj.user = request.user
        obj.save()
        form = PatientForm()
        data['form_is_valid'] = True
        
        # title = form.cleaned_data['title']    
        # obj = BlogPost.objects.create(title=title)  you can create and save this column data in multiple models
    context = {"form": form}
    data['html_form'] = render_to_string('settings/patients/modal/modal-create.html', context, request=request)
    
    return JsonResponse(data)

@login_required(login_url='signin')
def UpdatePatient(request, slug):
    patient = Patient.objects.get(slug=slug)
    form = PatientForm(request.POST or None, instance=patient) # To locate specific date instance=obj
    if form.is_valid():
            form.save()
            return redirect('patient-list')            
    template_name = 'settings/patients/update.html'
    context = {"form": form, "title": f"Update {patient.last_name}, - {patient.first_name}, {patient.middle_name}"  }
    return render(request, template_name, context)

@login_required(login_url='signin')
def DeletePatient(request, slug):
    patient = Patient.objects.get(slug=slug)
    template_name = 'settings/patients/delete.html'
    if request.method == "POST":
        patient.delete()
        return redirect('patient-list')
    context = {"patient": patient}
    return render(request, template_name, context)

''' -------------------------- HMOBill Section ---------------------------------'''  
@login_required(login_url='signin')
def HMOBillReport(request):
    hmo_bill_report = HMOBill.objects.filter(bill_status='Pending').order_by('-utility_date')
    
    charges = hmo_bill_report.values_list('charges', flat=True)
    professional_fee = hmo_bill_report.values_list('professional_fee', flat=True)
    credit = hmo_bill_report.values_list('credit', flat=True)
    total = hmo_bill_report.values_list('total', flat=True)

    total_charges = sum(charges)
    total_professional_fee = sum(professional_fee)
    total_credit = sum(credit)
    total_balance = sum(total)   
    
    context = {
        'hmo_bill_report': hmo_bill_report,
        'total_charges': total_charges,
        'total_professional_fee': total_professional_fee,
        'total_credit': total_credit,
        'total_balance': total_balance
        }

    template_name = 'settings/hmo-bills/reports.html'
    return render(request, template_name, context)

@login_required(login_url='signin')
def HMOBillList(request):

    hmo_bills = HMOBill.objects.all()
    context = {'hmo_bills': hmo_bills}
    template_name = 'settings/hmo-bills/list.html'
    return render(request, template_name, context)

@login_required(login_url='signin')
def HMOBillDetail(request, slug):

    hmo_bill_detail = HMOBill.objects.get(slug=slug)

    context = {'hmo_bill': hmo_bill_detail}
    template_name = 'settings/hmo-bills/detail.html'
    return render(request, template_name, context)

@login_required(login_url='signin')
def CreateHMOBill(request):
    qs = Doctor.objects.all()
    hmo_bill_list = HMOBill.objects.all().order_by('-date_created')
    form = HMOBillForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # obj.title = form.cleaned_data.get('title') + "0" can manipulat pre existing data
        obj.user = request.user
        obj.save()
        form = HMOBillForm()
        return redirect('create-hmo-bill')
        
        # title = form.cleaned_data['title']    
        # obj = BlogPost.objects.create(title=title)  you can create and save this column data in multiple models
    template_name = 'settings/hmo-bills/create.html'
    context = {"form": form, 'qs': qs, 'hmo_bill_list': hmo_bill_list}
    return render(request, template_name, context)


def CreateHMOBillPost(request):    
    if request.is_ajax and request.method == 'POST':
        form = HMOBillForm(request.POST)
        if form.is_valid():            
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({'instance': ser_instance, }, status=200)
        else:
            return JsonResponse({'error': form.errors}, status=400)            

    return JsonResponse({'error': ''}, status=400)


@login_required(login_url='signin')
def UpdateHMOBillModal(request, slug):
    data = dict()
    hmo_bill = HMOBill.objects.get(slug=slug)
    form = HMOBillForm(request.POST or None, instance=hmo_bill)
    if form.is_valid():
        # obj.title = form.cleaned_data.get('title') + "0" can manipulat pre existing data        
        form.save()
        data['form_is_valid'] = True        
        # title = form.cleaned_data['title']    
        # obj = BlogPost.objects.create(title=title)  you can create and save this column data in multiple models
    context = {"form": form}
    data['html_form'] = render_to_string('settings/hmo-bills/modal/modal-update.html', context, request=request)
    
    return JsonResponse(data)


@login_required(login_url='signin')
def UpdateHMOBill(request, slug):
    hmo_bill = HMOBill.objects.get(slug=slug)
    form = HMOBillUpdateForm(request.POST or None, instance=hmo_bill) # To locate specific date instance=obj
    if form.is_valid():
            form.save()
            return redirect('create-hmo-bill')            
    template_name = 'settings/hmo-bills/update.html'
    context = {"form": form, "title": f"Update {hmo_bill.hmo}, - {hmo_bill.patient}, {hmo_bill.approval_number}"  }
    return render(request, template_name, context)

@login_required(login_url='signin')
def DeleteHMOBill(request, slug):
    hmo_bill = HMOBill.objects.get(slug=slug)
    template_name = 'settings/patients/delete.html'
    if request.method == "POST":
        hmo_bill.delete()
        return redirect('create-hmo-bill')
    context = {"hmo_bill": hmo_bill}
    return render(request, template_name, context)

@login_required(login_url='signin')
def CreateSOA(request):

    form = SOAForm(request.POST or None)
    hmo_bills = HMOBill.objects.all()

    myFilter = HMOBillFilter(request.GET, queryset=hmo_bills)
    hmo_bills = myFilter.qs

    if request.method == "POST":
        form = SOAForm(request.POST or None)
        hmo_bill_list_id = request.POST.getlist('check-status')
        list_of_obj = HMOBill.objects.filter(pk__in=hmo_bill_list_id)       
        list_of_obj.update(bill_status='Pending')
        SOA.objects.bulk_create([SOA(hmo_bill=x) for x in list_of_obj])
        return redirect('soa-list')

    template_name = 'settings/hmo-bills/list-update.html'
    context = {"form": form, 'hmo_bills': hmo_bills, 'myFilter': myFilter }
    return render(request, template_name, context)




'''------------------ Is this Correct? ----------------'''

    # form = SOAForm(request.POST or None)
    # hmo_bills = HMOBill.objects.all()

    # if request.method == "POST":
    #     form = SOAForm(request.POST or None)
    #     hmo_bill_list_id = request.POST.getlist('check-status')
    #     list_of_obj = HMOBill.objects.get(id=hmo_bill_list_id[0])
    #     soa = SOA.objects.create(hmo_bill=list_of_obj)
    #     soa.save()   



'''-------------------------- Queryset Instance ----------------------'''

    # hmo_bill_list_id = request.POST.getlist('check-status')


    # list_of_obj = HMOBill.objects.filter(pk__in=hmo_bill_list_id)
    # if request.method == "POST":
    #     form = SOAForm(request.POST or None)
    #     if form.is_valid():
    #         soa = form.save(commit=False)
    #         soa.hmo_bill = HMOBill.objects.get(pk=list_of_obj)
            # soa.save()

''' --------------------- For Loop queryset -------------------'''          
        # for i in list_of_obj:
        #     soa = SOA.objects.create(hmo_bill=i)
        #     soa.save()

@login_required(login_url='signin')
def SOAList(request):

    soas = SOA.objects.values('soa_number').distinct()

    template_name = 'settings/soa/list.html'
    context = {'soas': soas}
    return render(request, template_name, context)

@login_required(login_url='signin')
def SOADetail(request, soa_number):

    soa = SOA.objects.filter(soa_number=soa_number).order_by('-hmo_bill__patient__last_name', '-hmo_bill__utility_date')

    # hmo_bill_filter = HMOBill.objects.filter()

    charges = soa.values_list('hmo_bill__charges', flat=True)
    professional_fee = soa.values_list('hmo_bill__professional_fee', flat=True)
    credit = soa.values_list('hmo_bill__credit', flat=True)
    total = soa.values_list('hmo_bill__total', flat=True)
    
    # charges = hmo_bill_filter.values_list('charges', flat=True)
    # professional_fee = hmo_bill_filter.values_list('professional_fee', flat=True)
    # credit = hmo_bill_filter.values_list('credit', flat=True)
    # total = hmo_bill_filter.values_list('total', flat=True)

    total_charges = sum(charges)
    total_professional_fee = sum(professional_fee)
    total_credit = sum(credit)
    total_balance = sum(total)

    template_name = 'settings/soa/detail.html'
    # context = {'soa': soa}
    

    context = {
    'soa': soa,
    'total_charges': total_charges,
    'total_professional_fee': total_professional_fee,
    'total_credit': total_credit,
    'total_balance': total_balance
    }

    return render(request, template_name, context)



