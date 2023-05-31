from django.forms import DateInput
from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Post, Category


class PostFilter(FilterSet):
    title = CharFilter(field_name='title',
                       lookup_expr='icontains',
                       label='Заголовок:')

    categories = ModelChoiceFilter(queryset=Category.objects.all(),
                                   label='Категория:',
                                   empty_label='Все категории')

    time = DateFilter(field_name='time',
                      lookup_expr='date',
                      widget=DateInput(attrs={'type': 'date'}),
                      label='Дата публикации:',)

    class Meta:
        model = Post
        fields = ['title', 'categories', 'time']
