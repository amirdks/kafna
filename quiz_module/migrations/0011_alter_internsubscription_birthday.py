# Generated by Django 4.2.2 on 2023-07-09 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_module', '0010_alter_internsubscription_fields_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internsubscription',
            name='birthday',
            field=models.DateField(verbose_name='تاریخ تولد'),
        ),
    ]
