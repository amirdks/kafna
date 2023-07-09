from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from quiz_module.validators import is_valid_iran_code, validate_file_extension


class InternField(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان رشته")
    english_title = models.CharField(max_length=255, verbose_name="عنوان انگلیسی رشته")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'رشته کارآموزی'
        verbose_name_plural = 'رشته های کارآموزی'


class JobSeekerField(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان رشته")
    english_title = models.CharField(max_length=255, verbose_name="عنوان انگلیسی رشته")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'رشته کارجو'
        verbose_name_plural = 'رشته های کارجو'


# Create your models here.
class InternSubscription(models.Model):
    EDUCATIONAL_FIELD = [
        ("HS", "دبیرستان"),
        ("VS", "هنرستان")
    ]
    EDUCATIONAL_STAGE = [
        ("tenth", "دهم"),
        ("eleventh", "یازدهم"),
        ("twelfth", "دوازدهم"),
    ]
    user = models.ForeignKey("account_module.User", on_delete=models.CASCADE, verbose_name="کاربر")
    birthday = models.DateField(verbose_name="تاریخ تولد")
    fields = models.ManyToManyField("InternField", blank=True, null=True, verbose_name="رشته های انتخابی")
    educational_field = models.CharField(choices=EDUCATIONAL_FIELD, max_length=2)
    student_code = models.CharField(max_length=255, verbose_name="شماره دانش آموزی")
    school_name = models.CharField(max_length=255, verbose_name="نام دبیرستان / هنرستان")
    educational_stage = models.CharField(choices=EDUCATIONAL_STAGE, max_length=10, verbose_name="مقطع تحصیلی")
    parent_phone_number = models.CharField(max_length=13, unique=True)
    email = models.EmailField(max_length=255, verbose_name="ایمیل")
    image_file = models.FileField(upload_to="image_file",
                                  verbose_name="فایل تصویر",
                                  validators=[validate_file_extension])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ثبت نام کارآموز'
        verbose_name_plural = 'ثبت نام های کارآموز'

    def __str__(self):
        return self.user.full_name


class JobSeekerSubscription(models.Model):
    user = models.ForeignKey("account_module.User", on_delete=models.CASCADE, verbose_name="کاربر")
    university_name = models.CharField(max_length=255, verbose_name="نام دانشگاه")
    field_of_study = models.CharField(max_length=255, verbose_name="رشته تحصیلی")
    email = models.EmailField(max_length=255, verbose_name="ایمیل")
    fields = models.ManyToManyField("JobSeekerField", blank=True, null=True, verbose_name="رشته های انتخابی")
    image_file = models.FileField(upload_to="image_file",
                                  verbose_name="فایل تصویر",
                                  validators=[validate_file_extension])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ثبت نام کارجو'
        verbose_name_plural = 'ثبت نام های کارجو'

    def __str__(self):
        return self.user.full_name


class Quiz(models.Model):
    field = models.ForeignKey(
        to="InternField",
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
    question = models.TextField(verbose_name="سوال")
    option_1 = models.TextField(verbose_name="گزینه اول")
    option_2 = models.TextField(verbose_name="گزینه دوم")
    option_3 = models.TextField(verbose_name="گزینه سوم")
    option_4 = models.TextField(verbose_name="گزینه چهارم")
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
