from django.contrib import admin
from .models import Product
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'discount', 'in_have', 'category')
    list_filter = ('category', 'in_have')
    search_fields = ('title', 'description')

    