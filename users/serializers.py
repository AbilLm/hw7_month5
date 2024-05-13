from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from users.models import ConfirmationCode


class UserAbstractSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(min_length=3)
class UserRegistrationSerializer(UserAbstractSerializer):

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('Пользователь с таким именем уже есть!')

class ConfirmationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmationCode
        fields = '__all__'
class UserAuthorizationSerializer(UserAbstractSerializer):
    pass