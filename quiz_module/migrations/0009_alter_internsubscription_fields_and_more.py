# Generated by Django 4.2.2 on 2023-07-09 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_module', '0008_internfield_jobseekerfield_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internsubscription',
            name='fields',
            field=models.ManyToManyField(null=True, to='quiz_module.internfield', verbose_name='رشته های انتخابی'),
        ),
        migrations.AlterField(
            model_name='jobseekersubscription',
            name='fields',
            field=models.ManyToManyField(null=True, to='quiz_module.jobseekerfield', verbose_name='رشته های انتخابی'),
        ),
    ]
