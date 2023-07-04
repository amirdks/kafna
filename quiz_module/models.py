from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from quiz_module.validators import is_valid_iran_code, validate_file_extension


class QuizField(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان فیلد")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'رشته'
        verbose_name_plural = 'رشته ها'


# Create your models here.
class QuizSubscription(models.Model):
    user = models.ForeignKey("account_module.User", on_delete=models.CASCADE, verbose_name="کاربر")
    field = models.ForeignKey(to="QuizField", help_text="این فیلد اجباری میباشد", related_name="first_field",
                              on_delete=models.CASCADE,
                              verbose_name="رشته انتخابی اول")
    field_2 = models.ForeignKey(to="QuizField", related_name="second_field", null=True, blank=True,
                                on_delete=models.CASCADE,
                                help_text="میتوانید این مورد را خالی بگذارید",
                                verbose_name="رشته انتخابی دوم")
    field_3 = models.ForeignKey(to="QuizField", help_text="میتوانید این مورد را خالی بگذارید",
                                related_name="third_field", null=True, blank=True,
                                on_delete=models.CASCADE,
                                verbose_name="رشته انتخابی سوم")
    image_file = models.FileField(upload_to="image_file",
                                  verbose_name="فایل تصویر",
                                  validators=[validate_file_extension])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ثبت نام آزمون'
        verbose_name_plural = 'ثبت نام های آزمون'

    def __str__(self):
        return self.user.full_name


class Quiz(models.Model):
    field = models.ForeignKey(
        to="QuizField",
        on_delete=models.CASCADE,
        verbose_name="رشته انتخابی اول"
    )
    description = models.TextField(verbose_name="توضیحات تست")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.field.title

    class Meta:
        verbose_name = 'آزمون'
        verbose_name_plural = 'آزمون ها'


class QuizQuestion(models.Model):
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE)
    question_1 = models.TextField(verbose_name="سوال اول")
    question_2 = models.TextField(verbose_name="سوال دوم")
    question_3 = models.TextField(verbose_name="سوال سوم")
    question_4 = models.TextField(verbose_name="سوال چهارم")
    answer_number = models.PositiveSmallIntegerField(validators=[
        MaxValueValidator(4),
        MinValueValidator(1)
    ])

    class Meta:
        verbose_name = 'سوالات آزمون'
        verbose_name_plural = 'سوالات آزمون ها'

    def __str__(self):
        return self.quiz.field.title


class QuizAnswer(models.Model):
    user = models.ForeignKey("account_module.User", on_delete=models.CASCADE)
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE)
    correct_percent = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(4),
            MinValueValidator(1)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'پاسخ کاربر'
        verbose_name_plural = 'پاسخ کاربران'

    def __str__(self):
        return f"{self.user.full_name} ==> {self.quiz.field.title}"
