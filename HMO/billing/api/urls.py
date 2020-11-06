from django.urls import path, re_path

from . import views

from .views import *


urlpatterns = [

    # '''--------------- PATIENT URL API --------------'''  
    path('patient/', views.PatientListAPI, name='patient-list-api'),
    path('patient/<slug>/', views.PatientDetailAPI, name='patient-detail-api'),
    path('patient/<slug>/update', views.PatienUpdateAPI, name='patient-update-api'),
    path('patient/<slug>/delete', views.PatientDeleteAPI, name='patient-delete-api'),
    path('patient/create', views.PatientCreateAPI, name='patient-create-api'),

    # '''--------------- ITEM URL API --------------'''    

    path('item/<slug>/', views.ItemDetailAPI, name='item-detail-api'),
    path('item/<slug>/update', views.ItemUpdateAPI, name='item-update-api'),
    path('item/<slug>/delete', views.ItemDeleteAPI, name='item-delete-api'),
    path('item/create', views.ItemCreateAPI, name='item-create-api'),

    # '''---------------- HMO BILL API ------------------'''

    path('hmo/', views.HMOBillListAPI, name='hmo-bill-list-api'),
]
