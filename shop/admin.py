from django.contrib import admin

from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    list_filter = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category','name','price']
    list_filter = ['category','name', 'publish']
    filter_horizontal = ('characteristics',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ['admin_name','name','value']
    list_filter = ['name', 'value']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'product', 'body')
