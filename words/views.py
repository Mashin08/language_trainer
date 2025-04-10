from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Word
from .forms import CategoryForm, WordForm
from django.contrib import messages

def home(request):
    return render(request, 'words/home.html')

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'words/category_list.html', {'categories': categories})

def word_list(request):
    words = Word.objects.all()
    return render(request, 'words/word_list.html', {'words': words})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Категория успешно добавлена")
            return redirect('category_list')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме")
    else:
        form = CategoryForm()
    return render(request, 'words/add_category.html', {'form': form})

def add_word(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Слово успешно добавлено")
            return redirect('word_list')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме")
    else:
        form = WordForm()
    return render(request, 'words/add_word.html', {'form': form})


def words_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    words = Word.objects.filter(category=category)
    return render(request, 'words/words_by_category.html', {'category': category, 'words': words})