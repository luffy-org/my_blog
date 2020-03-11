from django import forms
from django.forms import TextInput

from article.models import ArticlePost


class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = {'title', 'body'}
        # widgets = {
        #     'title': TextInput(attrs={'class': 'form-control'}),
        #     'body': forms.Textarea(attrs={'class': 'form-control'})
        # }

