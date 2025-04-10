from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Word

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('original', 'translation', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('original', 'translation')
    date_hierarchy = 'created_at'