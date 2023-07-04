# Generated by Django 4.2 on 2023-07-03 16:04

from django.db import migrations, models
import django.db.models.deletion
import quiz_module.validators


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_module', '0002_quiz_field_2_quiz_field_3_alter_quiz_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='نام و نام خانوادگی')),
                ('national_code', models.CharField(max_length=10, unique=True, validators=[quiz_module.validators.is_valid_iran_code], verbose_name='کد ملی')),
                ('phone_number', models.CharField(max_length=13, unique=True, verbose_name='شماره تلفن همراه')),
                ('image_file', models.FileField(upload_to='image_file', validators=[quiz_module.validators.validate_file_extension], verbose_name='فایل تصویر')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('field', models.ForeignKey(help_text='این فیلد اجباری میباشد', on_delete=django.db.models.deletion.CASCADE, related_name='first_field', to='quiz_module.quizfield', verbose_name='رشته انتخابی اول')),
                ('field_2', models.ForeignKey(blank=True, help_text='میتوانید این مورد را خالی بگذارید', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='second_field', to='quiz_module.quizfield', verbose_name='رشته انتخابی دوم')),
                ('field_3', models.ForeignKey(blank=True, help_text='میتوانید این مورد را خالی بگذارید', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='third_field', to='quiz_module.quizfield', verbose_name='رشته انتخابی سوم')),
            ],
        ),
        migrations.DeleteModel(
            name='Quiz',
        ),
    ]