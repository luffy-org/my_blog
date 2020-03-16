from django import forms
from django.forms import TextInput

from article.models import ArticlePost


class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ['title', 'body', 'column', 'tag', 'avatar']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 12}),
            'column': forms.Select(attrs={'class': 'form-control'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.widgets.FileInput(attrs={'class': 'form-control-file'})
        }

