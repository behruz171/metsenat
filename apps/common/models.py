from django.db import models
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User
from .apps import User



JISMONIY, YURIDIK = 'jismon', 'yuridik'
NEW, ACTIVE, CANCELED, MODERATION = 'new', 'active', 'cancelled', 'moderation'

BAKLAVR, MAGESTR, ASPERANT = 'baklavr', 'magestr', 'asperant'

phone_validator = RegexValidator(regex=r'^\+998\d{9}$', message='Iltimos Togri kiriting :)', code='invalid')


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Sponsor(BaseModel):
    TYPE_CHOICES = (
        (JISMONIY, 'Jismoniy Shaxs'),
        (YURIDIK, 'Yuridik Shaxs')
    )

    STATUS_CHOICES = (
        (NEW, 'New'),
        (CANCELED, 'Canceled'),
        (MODERATION, 'Moderation'),
        (ACTIVE, 'Active')   
    )

    name = models.CharField(max_length=233, verbose_name='Name')
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Amount')
    phone = models.CharField(
        max_length=50, verbose_name='Phone',
        validators=[phone_validator]
    )
    type = models.CharField(
        max_length=50, verbose_name='Type',
        choices=TYPE_CHOICES, default=JISMONIY
    )
    status = models.CharField(
        default=NEW, verbose_name='Status',
        max_length=255, choices=STATUS_CHOICES
    )
    company_name = models.CharField(max_length=233, null=True, blank=True)
    def __str__(self) -> str:
        return self.name


class Student(BaseModel):
    TYPE_CHOICES = (
        (BAKLAVR, 'baklavr'),
        (MAGESTR, 'magestr'),
        (ASPERANT, 'asperant') 
    )
    
    name = models.CharField(max_length=233, verbose_name='Student Name')
    phone = models.CharField(
        max_length=50, verbose_name='Phone',
        validators=[phone_validator]
    )
    contract = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Contract')
    type = models.CharField(
        max_length=50, verbose_name='Type',
        choices=TYPE_CHOICES, default=BAKLAVR
    )
    university = models.ForeignKey(
        'University',
        on_delete=models.PROTECT,
        related_name='students',
        verbose_name='University'
    )
    def __str__(self) -> str:
        return self.name

class University(BaseModel):
    name = models.CharField(max_length=233, verbose_name='Name')
    def __str__(self) -> str:
        return self.name


class AllocatedAmount(BaseModel):
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Amount')
    student = models.ForeignKey(
        Student, on_delete=models.PROTECT,
        related_name='sponsor_amounts',
        verbose_name='Student'
    )
    sponsor = models.ForeignKey(
        Sponsor, on_delete=models.PROTECT, related_name='sponsor_amounts',
        verbose_name='Sponsor'
    )

    def __str__(self) -> str:
        return self.sponsor.name


    