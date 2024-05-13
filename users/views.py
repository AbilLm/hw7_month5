import string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from .models import ConfirmationCode
from .serializers import UserRegistrationSerializer, UserAuthorizationSerializer, ConfirmationCodeSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random



def generate_confirmation_code():
    return ''.join(random.choices(string.digits, k=6))

@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = User.objects.create_user(username=username, password=password, is_active=False)

        confirmation_code = generate_confirmation_code()
        ConfirmationCode.objects.create(user=user, code=confirmation_code)

        # Отправка кода подтверждения пользователю (здесь ваш код для отправки)

        return Response(data={'confirmation_code': confirmation_code}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthorizationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def create_confirmation_code(request):
    user = request.user
    code = generate_confirmation_code()
    confirmation_code = ConfirmationCode.objects.create(user=user, code=code)
    return Response(data={'confirmation_code': code}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def confirm_user(request):
    code = request.data.get('code')
    try:
        confirmation_code = ConfirmationCode.objects.get(code=code)
        user = confirmation_code.user
        user.is_active = True
        user.save()
        confirmation_code.delete()
        return Response(data={'message': 'User confirmed successfully'}, status=status.HTTP_200_OK)
    except ConfirmationCode.DoesNotExist:
        return Response(data={'error': 'Invalid confirmation code'}, status=status.HTTP_400_BAD_REQUEST)