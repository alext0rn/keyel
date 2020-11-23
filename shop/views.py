from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Product, Category, Characteristic
from cart.forms import CartAddProductForm
from .forms import CommentForm


def index(request):
    return render(request, 'shop/index.html')

#Фильтры по характеристикам
class CharacteristicsView():
    #Комп'ютери
    def get_cpu(self):
        return Characteristic.objects.filter(name = 'Процесор')
    def get_graphiccard(self):
        return Characteristic.objects.filter(name = 'Відеокарта')
    def get_ramsize(self):
        return Characteristic.objects.filter(name = 'Об\'єм оперативної пам\'яті, ГБ')
    def get_harddrive(self):
        return Characteristic.objects.filter(name = 'Обсяг HDD, ГБ')
    def get_powersupply(self):
        return Characteristic.objects.filter(name = 'Блок живлення, ВТ')
    #Ноутбуки
    def get_nout_cpu(self):
        return Characteristic.objects.filter(filter_name = 'nout_cpu')
    def get_nout_graphiccard(self):
        return Characteristic.objects.filter(filter_name = 'nout_graphiccard')
    def get_nout_ramsize(self):
        return Characteristic.objects.filter(filter_name = 'nout_ramsize')
    def get_nout_harddrive(self):
        return Characteristic.objects.filter(filter_name = 'nout_harddrive')
    #Консолі
    def get_konsoli_manufacturer(self):
        return Characteristic.objects.filter(filter_name = 'konsoli_manufacturer')
    def get_konsoli_type(self):
        return Characteristic.objects.filter(filter_name = 'konsoli_type')
    def get_konsoli_harddrive(self):
        return Characteristic.objects.filter(filter_name = 'konsoli_harddrive')
    #Ігри
    def get_igri_platform(self):
        return Characteristic.objects.filter(filter_name = 'igri_platform')
    def get_igri_janr(self):
        return Characteristic.objects.filter(filter_name = 'igri_janr')

#Фильтрація для категорії комп'ютеры
class ComputerFilterView(CharacteristicsView, ListView):
    template_name = 'shop/products/list.html'
    context_object_name = 'products'
    paginate_by = 16

    def get_queryset(self):
        queryset = Product.objects.filter(
        Q(category__slug = 'kompyuteri'),
        Q(characteristics__value__in = self.request.GET.getlist("cpu")) |
        Q(characteristics__value__in = self.request.GET.getlist("graphiccard")) |
        Q(characteristics__value__in = self.request.GET.getlist("ram")) |
        Q(characteristics__value__in = self.request.GET.getlist("harddrive")) |
        Q(characteristics__value__in = self.request.GET.getlist("powersupply"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['current_category'] = Category.objects.get(slug = 'kompyuteri')
        return context

#Фильтрація для категорії ноутбуки
class NoutFilterView(CharacteristicsView, ListView):
    template_name = 'shop/products/list.html'
    context_object_name = 'products'
    paginate_by = 16

    def get_queryset(self):
        queryset = Product.objects.filter(
        Q(category__slug = 'noutbuki'),
        Q(characteristics__value__in = self.request.GET.getlist("cpu")) |
        Q(characteristics__value__in = self.request.GET.getlist("graphiccard")) |
        Q(characteristics__value__in = self.request.GET.getlist("ram")) |
        Q(characteristics__value__in = self.request.GET.getlist("harddrive"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['current_category'] = Category.objects.get(slug = 'noutbuki')
        return context

#Фильтрація для категорії ігрові консолі
class KonsoliFilterView(CharacteristicsView, ListView):
    template_name = 'shop/products/list.html'
    context_object_name = 'products'
    paginate_by = 16

    def get_queryset(self):
        queryset = Product.objects.filter(
        Q(category__slug = 'igrovi-konsoli'),
        Q(characteristics__value__in = self.request.GET.getlist("manufacturer")) |
        Q(characteristics__value__in = self.request.GET.getlist("type")) |
        Q(characteristics__value__in = self.request.GET.getlist("harddrive"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['current_category'] = Category.objects.get(slug = 'igrovi-konsoli')
        return context

#Фильтрація для категорії ігрові консолі
class IgriFilterView(CharacteristicsView, ListView):
    template_name = 'shop/products/list.html'
    context_object_name = 'products'
    paginate_by = 16

    def get_queryset(self):
        queryset = Product.objects.filter(
        Q(category__slug = 'igri-dlya-konsolej'),
        Q(characteristics__value__in = self.request.GET.getlist("platform")) |
        Q(characteristics__value__in = self.request.GET.getlist("janr"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['current_category'] = Category.objects.get(slug = 'igri-dlya-konsolej')
        return context

#Відображення товарів за категоріями
class ProductbyCategoryListView(CharacteristicsView, ListView):
    model = Product
    paginate_by = 16
    template_name = 'shop/products/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.order_by('-publish').filter(category__slug = self.kwargs['category_slug'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['current_category'] = Category.objects.get(slug = self.kwargs['category_slug'])
        return context

def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, category__slug = category_slug, slug = slug)
    cart_product_form = CartAddProductForm()
    comments = product.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.user_id = request.user.id
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'shop/products/detail.html', {'product':product, 'comment_form':comment_form,
'cart_product_form':cart_product_form,'new_comment':new_comment, 'comments': comments})
