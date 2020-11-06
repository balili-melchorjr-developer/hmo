from django.urls import path, reverse
from . import views

from .views import *

from django.conf.urls import url


from .models import *

urlpatterns = [

    

    # '''----------------------------- Item Section ------------------------'''

    path('items/', views.ItemList, name='item-list'),
    path('item/<str:slug>/', views.ItemDetail, name='item-detail'),
    path('create/item/', views.CreateItem, name='create-item'),
    path('item/<str:slug>/update', views.UpdateItem, name='update-item'),
    path('item/<str:slug>/delete', views.DeleteItem, name='delete-item'),

    # '''----------------------------- HMO Section ------------------------'''

    path('hmos/', views.HMOList, name='hmo-list'),
    path('hmo/<str:slug>/', views.HMODetail, name='hmo-detail'),
    path('create/hmo/', views.CreateHMO, name='create-hmo'),
    path('hmo/<str:slug>/update', views.UpdateHMO, name='update-hmo'),
    path('hmo/<str:slug>/delete', views.DeleteHMO, name='delete-hmo'),

    # '''----------------------------- Doctor Section ------------------------'''

    path('doctors/', views.DoctorList, name='doctor-list'),
    path('doctor/<str:slug>/', views.DoctorDetail, name='doctor-detail'),
    path('create/doctor/', views.CreateDoctor, name='create-doctor'),
    path('doctor/<str:slug>/update', views.UpdateDoctor, name='update-doctor'),
    path('doctor/<str:slug>/delete', views.DeleteDoctor, name='delete-doctor'),

    # '''----------------------------- Patient Section ------------------------'''

    path('patient/', views.PatientList, name='patient-list'),
    path('patient/<str:slug>/', views.PatientDetail, name='patient-detail'),
    path('create/patient/', views.CreatePatient, name='create-patient'),
    path('patient/<str:slug>/update', views.UpdatePatient, name='update-patient'),
    path('patient/<str:slug>/delete', views.DeletePatient, name='delete-patient'),

    # '''----------------------------- HMOBill Section ------------------------'''

    # path('hmo-bill-report/', views.HMOBillReport, name='hmo-bill-report'),
    # path('hmo-bill/', views.HMOBillList, name='hmo-bill-list'),

    path('hmo-bill/<str:slug>/', views.HMOBillDetail, name='hmo-bill-detail'),
    path('create-hmo-bill/', views.CreateHMOBill, name='create-hmo-bill'),
    path('hmo-bill-list-soa/', views.CreateSOA, name='hmo-bill-list-to-sia'),
    path('hmo-bill/<str:slug>/update', views.UpdateHMOBill, name='update-hmo-bill'),
    path('hmo-bill/<str:slug>/delete', views.DeleteHMOBill, name='delete-hmo-bill'),


    # ^^^^^^^^^^^^^^^^^^^^^^^^^^  AJAX  Section ^^^^^^^^^^^^^^^^^^^^^^^^^^^ 

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^ HMO BILL AJAX ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    path('post/ajax/create-hmo-bill-post', views.CreateHMOBillPost, name='create-hmo-bill-post'),
    path('post/ajax/update-hmo-bill-modal/<str:slug>/update', views.UpdateHMOBillModal, name='update-hmo-bill-modal'),


    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ PATIENT AJAX ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    path('post/ajax/create-patient-modal', views.CreatePatientModal, name='create-patient-modal'),


    # '''----------------------------- SOA Section ------------------------'''
    path('hmo-bills/', views.CreateSOA, name='hmo-bill-list'),
    path('soa-list/', views.SOAList, name='soa-list'),
    path('soa/<str:soa_number>/', views.SOADetail, name='soa-detail'),
]


urlpatterns += [
    url(r'^hmo-autocomplete/$', HMOAutocomplete.as_view(), name='hmo-autocomplete',),
    url(r'^patient-autocomplete/$', PatientAutocomplete.as_view(), name='patient-autocomplete',),
    url(r'^item-autocomplete/$', ItemAutocomplete.as_view(), name='item-autocomplete',),
    url(r'^doctor-autocomplete/$', DoctorAutocomplete.as_view(), name='doctor-autocomplete',),


]

