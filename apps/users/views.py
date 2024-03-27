from django.shortcuts import render
from rest_framework import viewsets, views, generics
from rest_framework.response import Response
from . import serializers



class SignUpView(generics.GenericAPIView):
    serializer_class = serializers.SignUpSerializer

def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=201)
