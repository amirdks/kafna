# Generated by Django 4.2.2 on 2023-07-09 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_module', '0009_alter_internsubscription_fields_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internsubscription',
            name='fields',
            field=models.ManyToManyField(blank=True, null=True, to='quiz_module.internfield', verbose_name='رشته های انتخابی'),
        ),
        migrations.AlterField(
            model_name='jobseekersubscription',
            name='fields',
            field=models.ManyToManyField(blank=True, null=True, to='quiz_module.jobseekerfield', verbose_name='رشته های انتخابی'),
        ),
    ]
