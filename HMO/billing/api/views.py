from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView

from account.models import *
from billing.models import *
from .serializers import *


''' ------------------------ PATIENT SECTION -----------------------'''

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def PatientListAPI(request):
    if request.method == 'GET':
        patient = Patient.objects.all().order_by('-last_name')
        serializers = PatientSerializer(patient, many=True)
        return Response(serializers.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def PatientDetailAPI(request, slug):
    try: 
        patient = Patient.objects.get(slug=slug)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def PatienUpdateAPI(request, slug):
    try:
        patient = Patient.objects.get(slug=slug)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if patient.user != user:
        return Response({'response': "You don't have permission to edit that"})

    if request.method == 'PUT':
        serializer = ItemSerializer(patient, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = 'update successful'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def PatientDeleteAPI(request, slug):
    try:
        patient = Patient.objects.get(slug=slug)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if patient.user != user:
        return Response({'response': "You don't have permission to edit that"})

    if request.method == 'DELETE':
        operation = patient.delete()
        data = {}
        if operation:
            data['success'] = 'delete successful'
        else:
            data['failure'] = 'delete failed'
        return Response(data=data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def PatientCreateAPI(request):

    user = request.user

    patient = Patient(user=user)

    if request.method == 'POST':
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


''' ------------------------ ITEM SECTION --------------------------- '''

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def ItemDetailAPI(request, slug):
    try:
        item = Item.objects.get(slug=slug)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def ItemUpdateAPI(request, slug):
    try:
        item = Item.objects.get(slug=slug)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if item.user != user:
        return Response({'response': "You don't have permission to edit that"})

    if request.method == 'PUT':
        serializer = ItemSerializer(item, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = 'update successful'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def ItemDeleteAPI(request, slug):
    try:
        item = Item.objects.get(slug=slug)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if item.user != user:
        return Response({'response': "You don't have permission to edit that"})

    if request.method == 'DELETE':
        operation = item.delete()
        data = {}
        if operation:
            data['success'] = 'delete successful'
        else:
            data['failure'] = 'delete failed'
        return Response(data=data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def ItemCreateAPI(request):

    user = request.user

    item = Item(user=user)

    if request.method == 'POST':
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


''' ------------------------ HMOBill SECTION --------------------------- '''


@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def HMOBillListAPI(request):
    if request.method == 'GET':
        hmo_bill_list = HMOBill.objects.all().order_by('-date_created')
        serializers = HMOBillSerializer(hmo_bill_list, many=True)
        return Response(serializers.data)




