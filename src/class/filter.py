import django_filters
from .models import Class


class ClassFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    more_info= django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Class
        fields = ['main_subject', 'place','day_one','day_two']
