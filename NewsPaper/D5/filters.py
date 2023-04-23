import django_filters
from django_filters import FilterSet, DateFromToRangeFilter
from django.forms import widgets
from .models import Post


class NewsFilter(FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name='dt_create', label='Дата',
                                                widget=widgets.SelectDateWidget,
                                                lookup_expr='gt')

                                                # LinkWidget(
                                                #     attrs={'input_type': 'Textarea',
                                                #            'template_name': 'django/forms/widgets/textarea.html'}))

    class Meta:
        model = Post
        fields = {'title': ['icontains'],  # использовал contains вместо exact потому что названия длинные
                  'text': ['icontains']}
