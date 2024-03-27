from typing import Any
from django.shortcuts import render
from.serializers import *
from rest_framework.generics import *
from rest_framework.views import Response
from . import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework import filters




class SponsorCreateAPIView(CreateAPIView):
    queryset = models.Sponsor.objects.all()
    serializer_class =SponsorCreateSerializer

class StudentSponsorCreateAPIView(CreateAPIView):
    queryset = models.AllocatedAmount.objects.all()
    serializer_class = StudentCreateSerializer

class StudentSponsorListAPIView(ListAPIView):
    queryset = models.AllocatedAmount.objects.all()
    serializer_class = StudentSponsorListSerializer
    


    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        return AllocatedAmount.objects.filter(student_id=student_id)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
class StudentListAPIView(ListAPIView):
    queryset = models.Student.objects.all()
    serializer_class = StudentListSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['university', 'type']
    search_fields = ['name']


class TotalAmountStatisticAPIView(APIView):
    def get(self, requests, *args, **kwargs):
        total_required_amount = Student.objects.aggregate(total=Sum('contract'))['total']
        total_paid_amount = AllocatedAmount.objects.aggregate(total=Sum('amount'))['total']
        return Response(
            data = {
                    'total_required_amount': total_required_amount,
                    'total_paid_amount': total_paid_amount,
                    'total_ramain_amount':total_required_amount - total_paid_amount
            }
        )
    
class MonthlyStatisticAPIView(APIView):


    def get(self, requests, *args, **kwargs):
        from datetime import date
        this_year = date.today().year

        # students = Student.objects.all()
        # sponsor = Sponsor.objects.all()


        results = []
        for i in range(1, 13):
            results.append({
                'month':self.get_month(i),
                'students':Student.objects.filter(created_at__month=i).count(),
                'sponsors':Sponsor.objects.filter(created_at__month=i).count()

            })
        return Response(results)

    def get_month(self, month_in_number):
        l = {
            1: 'Yanvar',
            2: 'Fevral',
            3: 'Mart',
            4: 'Aprel',
            5: 'May',
            6: 'Iyun',
            7: 'Iyul',
            8: 'Avgust',
            9: 'Sentyabr',
            10: 'Oktyabr',
            11: 'Noyabr',
            12: 'Dekabr'
        }
        return l[month_in_number]
    

class SponsorListAPIView(ListAPIView):
    queryset = models.Sponsor.objects.all()
    serializer_class = SponsorListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name', 'type']
    search_fields = ['name']


from rest_framework import generics
from .models import Sponsor
from .serializers import SponsorSerializer

# class SponsorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Sponsor.objects.all()
#     serializer_class = SponsorSerializer

class AllocatedAmountUpdateAPIView(RetrieveUpdateAPIView):
    queryset = AllocatedAmount.objects.all()
    serializer_class = AllocatedAmountUpdateSerializer
