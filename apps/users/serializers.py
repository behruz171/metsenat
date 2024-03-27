from rest_framework import serializers
import re
from  . import models

def validator(value):
    regex = r"^\+998\d{9}$"
    if not re.fullmatch(regex, value):
        raise serializers.ValidationError({'msg': 'Not a valid phone number'})

class SignUpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=13, min_length=13, validators = [validator]
    )
    password = serializers.CharField(write_only = True)


    def create(self, validated_data):
        phone = validated_data.get('phone_number')
        password = validated_data.get('password')
        user = models.User.objects.filter(phone_number=phone).first()
        if user:
            raise serializers.ValidationError({'msg': 'This phone number already exists'})

        user = models.User.objects.create_user(phone_number=phone, password=password)
        return user
    

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tokens'] = instance.tokens()
        return data
    









