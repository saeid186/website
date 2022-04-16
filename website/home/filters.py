import django_filters
from django import forms
from .models import *


class ProductFilter(django_filters.FilterSet):
    price_1 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    price_2 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='lte')
