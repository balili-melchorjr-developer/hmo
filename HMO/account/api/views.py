from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token


from account.api.serializers import *

@api_view(['POST',])
def SignUpAPI(request):
    
    if request.method == 'POST':
        serializers = SignUpSerializers(data=request.data)
        data = {} # This is like Context { 'name': assign variable }
        if serializers.is_valid():
            account = serializers.save()
            data['response'] = 'Successfully registered a new user'
            data['email'] = account.email
            data['last_name'] = account.last_name
            data['first_name'] = account.first_name
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializers.errors
        return Response(data)
