from django.urls import path

from .views import index, ProductbyCategoryListView, ComputerFilterView, NoutFilterView, KonsoliFilterView, IgriFilterView, product_detail

app_name = 'shop'

urlpatterns = [
    path('filter_comp/', ComputerFilterView.as_view(), name = 'computers_filter'),
    path('filter_nout/', NoutFilterView.as_view(), name = 'nout_filter'),
    path('filter_konsoli/', KonsoliFilterView.as_view(), name = 'konsoli_filter'),
    path('filter_igri/', IgriFilterView.as_view(), name = 'igri_filter'),
    path('<slug:category_slug>/', ProductbyCategoryListView.as_view(), name = 'product_list_by_category'),
    path('<slug:category_slug>/<slug:slug>/', product_detail, name = 'product_detail'),
    path('', index, name = 'index'),
]
