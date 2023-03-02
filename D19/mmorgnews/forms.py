from django import forms
from .models import Post, Comment
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    # title = forms.CharField(min_length=255)
    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'text',
            'author'
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title is not None and len(title) > 255:
            raise ValidationError({'title': 'Название новости не может быть длиннее 255 символов'})


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text'
        ]
