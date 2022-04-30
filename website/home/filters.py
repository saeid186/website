import django_filters
from django import forms
from .models import *


class ProductFilter(django_filters.FilterSet):
    choice_one = (
        ('گرانترین', 'گرانترین'),
        ('ارزانترین', 'ارزانترین')
    )

    choice_two = (
        ('old', 'قدیمی'),
        ('جدیدترین', 'جدیدترین')
    )

    choice_three = (
        ('dis', 'کم تخفیف'),
        ('بیشترین تخفیف', 'بیشترین تخفیف')
    )
    price_1 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    price_2 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='lte')
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
    price = django_filters.ChoiceFilter(choices=choice_one, method='price_filter')
    create = django_filters.ChoiceFilter(choices=choice_two, method='create_filter')
    discount = django_filters.ChoiceFilter(choices=choice_three, method='discount_filter')

    def price_filter(self, queryset, name, value):
        data = 'unit_price' if value == 'ارزانترین' else '-unit_price'
        return queryset.order_by(data)

    def create_filter(self, queryset, name, value):
        data = 'create' if value == 'old' else '-create'
        return queryset.order_by(data)

    def discount_filter(self, queryset, name, value):
        data = 'discount' if value == 'dis' else '-discount'
        return queryset.order_by(data)

