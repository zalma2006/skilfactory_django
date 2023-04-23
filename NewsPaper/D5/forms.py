from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class NewsForm(forms.ModelForm):
    # title = forms.CharField(min_length=255)
    class Meta:
        model = Post
        fields = [
            'changes',
            'category_id',
            'title',
            'text',
            'author_id'
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title is not None and len(title) > 255:
            raise ValidationError({'title': 'Название новости не может быть длиннее 255 символов'})
