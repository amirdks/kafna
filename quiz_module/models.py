from django.db import models

from quiz_module.validators import is_valid_iran_code, validate_file_extension


class QuizField(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان فیلد")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # class Meta:
    #     verbose_name = ''
    #     verbose_name_plural = ''


# Create your models here.
class Quiz(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی")
    national_code = models.CharField(max_length=10, unique=True, validators=[is_valid_iran_code], verbose_name='کد ملی')
    phone_number = models.CharField(max_length=13, unique=True, verbose_name='شماره تلفن همراه')
    field = models.ForeignKey(to="QuizField", on_delete=models.CASCADE, verbose_name="رشته انتخابی")
    image_file = models.FileField(upload_to="image_file", verbose_name="فایل تصویر",
                                  validators=[validate_file_extension])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
