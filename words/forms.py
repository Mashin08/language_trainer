from django import forms
from .models import Category, Word


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['original', 'translation', 'transcription', 'example', 'category']
        widgets = {
            'original': forms.TextInput(attrs={'class': 'form-control'}),
            'translation': forms.TextInput(attrs={'class': 'form-control'}),
            'transcription': forms.TextInput(attrs={'class': 'form-control'}),
            'example': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_original(self):
        original = self.cleaned_data['original']
        if len(original) < 2:
            raise forms.ValidationError("Слово должно содержать минимум 2 символа")
        return original

    def clean_translation(self):
        translation = self.cleaned_data['translation']
        if len(translation) < 2:
            raise forms.ValidationError("Перевод должен содержать минимум 2 символа")
        return translation