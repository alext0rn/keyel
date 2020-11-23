from django import template
from django.db.models import Count

from ..models import Product


register = template.Library()

@register.inclusion_tag('shop/products/latest.html')
def show_latest_products(count=4):
    latest_products = Product.objects.order_by('-publish')[:count]
    return {'latest_products': latest_products}

@register.inclusion_tag('shop/products/most.html')
def show_most_products(count=4):
    most_products = Product.objects.annotate(total_comments=Count('comments')).order_by('-total_comments').distinct()[:count]
    return {'most_products': most_products}
