# Generated by Django 4.2.2 on 2023-07-10 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0002_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='phone_number',
            field=models.CharField(max_length=13),
        ),
    ]