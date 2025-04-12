from django.db.models.functions import Cast
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Word
from .forms import CategoryForm, WordForm
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, ExpressionWrapper, FloatField, F
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils import timezone

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
        categories = Category.objects.filter(Q(user=request.user))
    else:
        categories = Category.objects.filter(user__isnull=True)
    return render(request, 'words/category_list.html', {'categories': categories})


def word_list(request):
    learned_filter = request.GET.get('learned', None)

    if request.user.is_authenticated:
        words = Word.objects.filter(Q(user=request.user))
    else:
        words = Word.objects.filter(user__isnull=True)

    if learned_filter == 'true':
        words = words.filter(learned=True)
    elif learned_filter == 'false':
        words = words.filter(learned=False)

    return render(request, 'words/word_list.html', {
        'words': words,
        'learned_filter': learned_filter
    })

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, user=request.user)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, "Категория успешно добавлена")
            return redirect('category_list')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме")
    else:
        form = CategoryForm(user=request.user)

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

    by_category = (
        words.values('category__name')
        .annotate(
            total=Count('id'),
            learned=Count('id', filter=Q(learned=True)),
        )
        .annotate(  # Второй annotate для расчета процента
            percent=ExpressionWrapper(
                F('learned') * 100.0 / F('total'),
                output_field=FloatField()
            )
        )
    ).order_by('-percent')

    stats = {
        'total': words.count(),
        'learned': words.filter(learned=True).count(),
        'learned_percent': int(100 * words.filter(learned=True).count() / words.count()),
        'to_learn_percent': 100 - int(100 * words.filter(learned=True).count() / words.count()),
        'to_learn': words.filter(learned=False).count(),
        'by_category': by_category,
        'recent': words.order_by('-last_reviewed')[:5],
    }

    return render(request, 'words/stats.html', {'stats': stats})


@require_POST
@login_required
def toggle_learned_status(request, word_id):
    word = get_object_or_404(Word, id=word_id, user=request.user)
    word.learned = not word.learned
    word.learned_date = timezone.now() if word.learned else None
    word.save()

    return JsonResponse({
        'success': True,
        'learned': word.learned,
        'updated_date': word.learned_date.strftime('%Y-%m-%d') if word.learned_date else None
    })

@login_required
def edit_word(request, word_id):
    word = get_object_or_404(Word, id=word_id, user=request.user)

    if request.method == 'POST':
        form = WordForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            messages.success(request, "Слово успешно обновлено")
            return redirect('word_list')
    else:
        form = WordForm(instance=word)

    return render(request, 'words/edit_word.html', {'form': form})