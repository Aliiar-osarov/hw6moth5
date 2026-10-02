from rest_framework import serializers
from .models import Product
from decimal import Decimal

class ProductSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField(
        help_text = "ИТОГОВАЯ ЦЕНА С УЧЕТОМ СКИДКИ"
    )

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'discount', 'in_have', 'category', 'description', 'final_price']
        read_only_fields = ['id', 'final_price']

    def get_final_price(self, obj) -> str:
        discount = (Decimal(obj.discount) / Decimal(100)) * obj.price
        result = obj.price - discount
        return f"{result:.2f}"

