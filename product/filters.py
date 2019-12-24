import django_filters

from product.models import Product, Comment, Category


class ProductFilter(django_filters.rest_framework.FilterSet):
    category = django_filters.AllValuesFilter(field_name='category__name')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    date_from = django_filters.DateFilter(field_name='created', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ('category', 'name', 'min_price', 'max_price', 'date_from', 'date_to')


class CommentFilter(django_filters.rest_framework.FilterSet):
    product = django_filters.AllValuesFilter(field_name='product__name')
    user = django_filters.AllValuesFilter(field_name='user__email')

    class Meta:
        model = Comment
        fields = ('product', 'user')


class CategoryFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.AllValuesFilter(field_name='name')

    class Meta:
        model = Category
        fields = ('name',)
