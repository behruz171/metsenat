# Generated by Django 5.0.3 on 2024-03-18 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='payment_type',
            field=models.CharField(choices=[('Karta_orqali', 'card'), ('Naqd_pul', 'Naqd pul')], default='Naqd_pul', max_length=250),
        ),
    ]