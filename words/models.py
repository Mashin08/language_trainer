from django.db import models
from django.core.validators import MinLengthValidator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Word(models.Model):
    original = models.CharField(max_length=100, verbose_name="Иностранное слово")
    translation = models.CharField(max_length=100, verbose_name="Перевод")
    transcription = models.CharField(max_length=100, blank=True, verbose_name="Транскрипция")
    example = models.TextField(blank=True, verbose_name="Пример использования")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.original} - {self.translation}"

    class Meta:
        verbose_name = "Слово"
        verbose_name_plural = "Слова"
        ordering = ['-created_at']