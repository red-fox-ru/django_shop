from itertools import product

import diagonal as diagonal
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name Category')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Image product')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')

    def __str__(self):
        return self.title


class RamProduct(Product):
    CHOICES_TYPE_RAM = (
        ('DDR2', 'DDR2'),
        ('DDR3', 'DDR3'),
        ('DDR4', 'DDR4'),
        ('DDR5', 'DDR5'),
    )

    type_ram = models.CharField(max_length=9, choices=CHOICES_TYPE_RAM)
    count_memory = models.IntegerField(validators=[
        MaxValueValidator(999),
        MinValueValidator(1)
    ], verbose_name='RAM GB')
    frequency = models.IntegerField(validators=[
        MaxValueValidator(99999),
        MinValueValidator(1)
    ], verbose_name='RAM frequency')

    class Meta:
        verbose_name = "Оперативная память"
        verbose_name_plural = "Оперативная память"


class NotebookProduct(Product):
    diagonal = models.CharField(max_length=225, verbose_name='Diagonal')
    display_type = models.CharField(max_length=255, verbose_name='Display')
    processor_frequency = models.DecimalField(max_digits=2, decimal_places=2, verbose_name='Processor Frequency')
    ram = models.ForeignKey(RamProduct, on_delete=models.SET_NULL, verbose_name='RAM', null=True)
    number_ram_slots = models.PositiveIntegerField(validators=[
        MaxValueValidator(8),
        MinValueValidator(1)
    ], verbose_name='Count slots RAM')
    max_memory = models.PositiveIntegerField(validators=[
        MaxValueValidator(999),
        MinValueValidator(1)
    ], verbose_name='Max volume GB RAM')
    free_slots = models.IntegerField(default=0, validators=[
        MaxValueValidator(8),
        MinValueValidator(0)
    ], verbose_name='Free slots RAM')
    graphics_element = models.CharField(max_length=255)
    time_without_charge = models.CharField(max_length=255, verbose_name='Time work accumulated')

    class Meta:
        verbose_name = "Ноутбук"
        verbose_name_plural = "Ноутбуки"

    def __str__(self):
        return f'{self.category.name}: {self.title}'


class SmartphoneProduct(Product):
    diagonal = models.CharField(max_length=225, verbose_name='Diagonal')
    display_type = models.CharField(max_length=255, verbose_name='Display')
    resolution = models.CharField(max_length=255, verbose_name='Screen Resolution')
    processor_frequency = models.DecimalField(max_digits=2, decimal_places=2, verbose_name='Processor Frequency')
    ram = models.CharField(max_length=255, verbose_name='Ram info')
    accum_volume = models.IntegerField(validators=[
        MaxValueValidator(99999),
        MinValueValidator(1)
    ], verbose_name='Accum Volume')
    sd = models.BooleanField(default=False, verbose_name='SD')
    sd_volume_max = models.IntegerField(validators=[
        MaxValueValidator(999),
        MinValueValidator(1)
    ], verbose_name='SD volume Gb')
    main_cam = models.IntegerField(validators=[
        MaxValueValidator(999),
        MinValueValidator(1)
    ], verbose_name='First camera Mp')
    front_cam = models.IntegerField(validators=[
        MaxValueValidator(999),
        MinValueValidator(1)
    ], verbose_name='Front camera Mp')

    class Meta:
        verbose_name = "Сматрфон"
        verbose_name_plural = "Смартфоны"

    def __str__(self):
        return f'{self.category.name}: {self.title}'


class CartProduct(models.Model):
    cart = models.ForeignKey('Cart', verbose_name='Basket', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total price')

    class Meta:
        verbose_name = "Продукт в корзину"
        verbose_name_plural = "Продукт в корзине"

    def __str__(self):
        return f'Product: {self.content_type}'


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name='Customer', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total')

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return str(self.id)
