from django.db import models
from decimal import Decimal #не целые числа 
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):

    class CategoryChoices(models.TextChoices):
        ELECTRONICS = 'electronics', 'Электроника'
        CLOTHES = 'clothe', 'Одежда'
        BOOKS = 'books', 'Книга'
        FOOD = 'food', 'Еда'
        OTHER = 'other', 'другое'

    title = models.CharField(max_length=155, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, 
                                validators=[MinValueValidator(Decimal('0.01'))],
                                verbose_name='Цена')
    discount = models.PositiveIntegerField(
        default=0 ,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='скидка (в процентах)'
    )
    category = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices,
        default=CategoryChoices.OTHER,
        verbose_name="Категория"
    )
    in_have = models.BooleanField(
        default=True,
        verbose_name="есть ли в наличии"
    )
    