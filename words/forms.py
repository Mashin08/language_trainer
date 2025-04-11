from django import forms
from .models import Category, Word
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Category.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Категория с таким названием уже существует")
        return name


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['original', 'translation', 'transcription', 'example', 'category']
        widgets = {
            'original': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[a-zA-Zа-яА-Я\- ]{2,}',
                'title': 'Только буквы и дефис, минимум 2 символа'
            }),
            'translation': forms.TextInput(attrs={
                'class': 'form-control',
                'minlength': '2'
            }),
            'transcription': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '\[.*\]',
                'title': 'Должно быть в квадратных скобках, например: [ˈwɔːtə]'
            }),
            'example': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        original = cleaned_data.get('original')
        translation = cleaned_data.get('translation')

        if original and translation and original.lower() == translation.lower():
            raise forms.ValidationError("Слово и перевод не должны быть одинаковыми")

        return cleaned_data

    def clean_original(self):
        original = self.cleaned_data['original']
        if Word.objects.filter(original__iexact=original).exists():
            raise forms.ValidationError("Такое слово уже существует в словаре")
        return original

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]