from django.db import transaction
from django.db.backends.utils import logger
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Category, Word


@receiver(post_save, sender=User)
def copy_base_data_to_new_user(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                # 1. Копируем категории с проверкой существования
                base_categories = Category.objects.filter(user__isnull=True)
                category_map = {}

                for cat in base_categories:
                    # Проверяем, нет ли уже такой категории у пользователя
                    if not Category.objects.filter(user=instance, name=cat.name).exists():
                        new_cat = Category.objects.create(
                            name=cat.name,
                            description=cat.description,
                            user=instance
                        )
                        category_map[cat.id] = new_cat.id

                # 2. Копируем слова
                base_words = Word.objects.filter(user__isnull=True)
                for word in base_words:
                    # Пропускаем слова, если категория не была скопирована
                    if word.category_id in category_map:
                        Word.objects.create(
                            original=word.original,
                            translation=word.translation,
                            transcription=word.transcription,
                            example=word.example,
                            category_id=category_map[word.category_id],
                            user=instance
                        )
        except Exception as e:
            logger.error(f"Error copying base data for user {instance.id}: {str(e)}")