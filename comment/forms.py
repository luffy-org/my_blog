from django import forms

from comment.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

        widgets = {
            'body': forms.widgets.Textarea(attrs={'class': 'form-control', 'rows': 12})
        }