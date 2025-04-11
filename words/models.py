from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название категории",
        validators=[
            MinLengthValidator(2, "Название категории должно содержать минимум 2 символа"),
            RegexValidator(
                regex='^[a-zA-Zа-яА-Я0-9 ]+$',
                message='Название категории может содержать только буквы и цифры'
            )
        ]
    )
    description = models.TextField(blank=True, verbose_name="Описание")

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ('user', 'name')


class Word(models.Model):
    original = models.CharField(
        max_length=100,
        verbose_name="Иностранное слово",
        validators=[
            MinLengthValidator(2, "Слово должно содержать минимум 2 символа"),
            RegexValidator(
                regex='^[a-zA-Zа-яА-Я\- ]+$',
                message='Слово может содержать только буквы и дефис'
            )
        ]
    )
    translation = models.CharField(
        max_length=100,
        verbose_name="Перевод",
        validators=[
            MinLengthValidator(2, "Перевод должен содержать минимум 2 символа")
        ]
    )
    transcription = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Транскрипция",
        validators=[
            RegexValidator(
                regex='^\[.*\]$',
                message='Транскрипция должна быть заключена в квадратные скобки, например: [ˈwɔːtə]'
            )
        ]
    )
    example = models.TextField(blank=True, verbose_name="Пример использования")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    learned = models.BooleanField(
        default=False,
        verbose_name="Выучено"
    )
    learned_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата изучения"
    )
    last_reviewed = models.DateTimeField(null=True, blank=True)
    review_count = models.IntegerField(default=0)

    def mark_learned(self):
        self.learned = True
        self.learned_date = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.original} - {self.translation}"

    class Meta:
        verbose_name = "Слово"
        verbose_name_plural = "Слова"
        ordering = ['-created_at']