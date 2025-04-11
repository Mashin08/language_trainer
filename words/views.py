from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Word
from .forms import CategoryForm, WordForm
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST


def home(request):
    return render(request, 'words/home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('word_list')
    else:
        form = RegisterForm()
    return render(request, 'words/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('word_list')
    else:
        form = AuthenticationForm()
    return render(request, 'words/login.html', {'form': form})


def category_list(request):
    if request.user.is_authenticated:
        categories = Category.objects.filter(Q(user=request.user) | Q(user__isnull=True))
    else:
        categories = Category.objects.filter(user__isnull=True)
    return render(request, 'words/category_list.html', {'categories': categories})


def word_list(request):
    if request.user.is_authenticated:
        words = Word.objects.filter(Q(user=request.user) | Q(user__isnull=True))
    else:
        words = Word.objects.filter(user__isnull=True)
    return render(request, 'words/word_list.html', {'words': words})


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, "Категория успешно добавлена")
            return redirect('category_list')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме")
    else:
        form = CategoryForm()

    return render(request, 'words/add_category.html', {
        'form': form,
        'title': 'Добавить новую категорию'
    })



@login_required
def add_word(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            # Сохраняем форму с commit=False, чтобы добавить пользователя
            word = form.save(commit=False)
            # Привязываем слово к текущему пользователю
            word.user = request.user
            # Сохраняем в базу
            word.save()
            # Сообщение об успехе
            messages.success(request, "Слово успешно добавлено")
            return redirect('word_list')
        else:
            # Сообщение об ошибке валидации
            messages.error(request, "Пожалуйста, исправьте ошибки в форме")
    else:
        form = WordForm()

    # Добавляем фильтрацию категорий по пользователю
    form.fields['category'].queryset = request.user.category_set.all()

    return render(request, 'words/add_word.html', {
        'form': form,
        'title': 'Добавить новое слово'
    })

def words_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    words = Word.objects.filter(category=category)
    return render(request, 'words/words_by_category.html', {'category': category, 'words': words})


@login_required
def stats(request):
    words = Word.objects.filter(user=request.user)

    stats = {
        'total': words.count(),
        'learned': words.filter(learned=True).count(),
        'to_learn': words.filter(learned=False).count(),
        'by_category': words.values('category__name').annotate(total=Count('id')),
        'recent': words.order_by('-last_reviewed')[:5],
    }

    return render(request, 'words/stats.html', {'stats': stats})
