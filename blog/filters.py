import django_filters

from .models import Organization


class OrganizationFilter(django_filters.FilterSet):
    price_from = django_filters.NumberFilter(field_name='budget', lookup_expr='gte')
    price_to = django_filters.NumberFilter(field_name='budget', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category')

    class Meta:
        model = Organization
        fields = ('price_from', 'price_to', 'category')



