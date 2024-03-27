from rest_framework import serializers
from .models import *

from django.db.models import Sum

class SponsorCreateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Sponsor
        exclude = ('status', 'payment_type', )


    def validate(self, attrs):
        university = attrs.get('university')
        user_type = attrs.get('user_type')


        return super().validate(attrs)


class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllocatedAmount
        fields = "__all__"


    def validate(self, attrs):
        student = attrs['student']
        # print(student)
        sponsor = attrs['sponsor']
        amount = attrs['amount']
        # print(amount)
        sponsor_corrent_amount  = sponsor.amount - sponsor.sponsor_amounts.all().aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        if sponsor_corrent_amount < amount:
            raise serializers.ValidationError('Sponsorda bunday pul mavjud emas')
        

        student_current_amount = student.contract - student.student_amounts.all().aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        # print(student_current_amount)

        if student_current_amount < amount:
            raise serializers.ValidationError('Studentga bu pul ortiqcha')


        

        

        return super().validate(attrs)


class StudentSponsorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllocatedAmount
        fields = "__all__"


class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'id',
            'name',
            'university',
            'contract',
            'type'
        )
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['allocated_amount'] = instance.student_amounts.all().aggregate(total_amount=Sum('amount')) or 0
        return data

class SponsorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = (
            'id',
            'name',
            'type'
        )
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['allocated_amount'] = instance.sponsor_amounts.all().aggregate(total_amount=Sum('amount')) or 0
        return data




class SponsorSerializer(serializers.ModelSerializer):
    # student = serializers.CharField(source='student.name')
    # print(student)

    class Meta:
        model = AllocatedAmount
        fields = '__all__'

class AllocatedAmountUpdateSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = AllocatedAmount
        fields = ["student", "sponsor", 'amount']

    def validate(self, attrs):
        student = attrs.get('student')
        sponsor = attrs.get('sponsor')
        amount = attrs.get('amount')
        sarflangan_summa = sponsor.sponsor_amounts.all().aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        sponsor_current_amount = sponsor.amount - sarflangan_summa

        if amount > sponsor_current_amount:
            raise serializers.ValidationError({'msg': f'Sponsorda  {sponsor_current_amount}  mablag bor'})
        
        student_current_amount = student.sponsor_amounts.all().aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        if student.contract - student_current_amount < amount:
            raise serializers.ValidationError({'msg': f'Studentda  {student.contract - student_current_amount} contract qoldi '})
        return super().validate(attrs)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['student'] = instance.student.name
        data['sponsor'] = instance.sponsor.name
        return data
