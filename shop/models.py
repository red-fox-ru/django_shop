import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from users.models import User


class MinResolutionValidation(Exception):
    pass


class MaxResolutionValidation(Exception):
    pass


class LatestProductsManager:

    @staticmethod
    def get_products_for_module(*args, **kwargs):
        with_respect_to = kwargs.get("with_respect_to")

        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for el_model in ct_models:
            model_products = el_model.model_class()._base_manager.all().order_by("-id")[:6]
            products.extend(model_products)

        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products,
                        key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to),
                        reverse=True
                    )

        return products


class LatestProducts:
    objects = LatestProductsManager()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name Category')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (800, 1280)

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Загаловок')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    year = models.PositiveIntegerField(validators=[
        MinValueValidator(1980)
    ])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        min_width, min_height = self.MIN_RESOLUTION
        max_width, max_height = self.MAX_RESOLUTION
        img = Image.open(self.image)
        if img.width < min_width or img.height < min_height:
            raise MinResolutionValidation('Разрешение изображения меньше минимального!')
        if img.width > max_width or img.height > max_height:
            new_image = img.convert('RGB')
            resized_img = new_image.resize((max_width, max_height), Image.ANTIALIAS)
            file_ = BytesIO()
            resized_img.save(file_, 'JPEG', quality=90)
            file_.seek(0)
            name = '{}.{}'.format(*self.img.name.split('.'))
            self.image = InMemoryUploadedFile(file_, 'ImageField', name, 'jpeg/image', sys.getsizeof(file_), None)
            super().save(*args, **kwargs)
            raise MaxResolutionValidation('Изображение слишком большое, оно было обрезано!')
        super().save(*args, *kwargs)


class RamProduct(Product):
    CHOICES_TYPE_RAM = (
        ('DDR2', 'DDR2'),
        ('DDR3', 'DDR3'),
        ('DDR4', 'DDR4'),
        ('DDR5', 'DDR5'),
    )

    type_ram = models.CharField(max_length=9, choices=CHOICES_TYPE_RAM, verbose_name='Тип памяти')
    count_memory = models.IntegerField(validators=[
        MaxValueValidator(999),
        MinValueValidator(1)
    ], verbose_name='Память GB')
    frequency = models.IntegerField(validators=[
        MaxValueValidator(99999),
        MinValueValidator(1)
    ], verbose_name='ОП частота GHz')

    class Meta:
        verbose_name = "Оперативная память"
        verbose_name_plural = "Оперативная память"


class Processor(Product):
    manufacturer = models.CharField(max_length=128, verbose_name='Производитель')
    soket = models.CharField(max_length=200, verbose_name='Сокет')
    frequency = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Частота процессора GHz')
    cores = models.PositiveIntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ], verbose_name='Количество ядер')
    graphics_core = models.BooleanField(default=False, blank=True, verbose_name="Графическое ядро")
    tdp = models.PositiveIntegerField(validators=[
        MaxValueValidator(900),
        MinValueValidator(10)
    ], verbose_name='Тепловыделение Вт')


class NotebookProduct(Product):
    diagonal = models.CharField(max_length=225, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Дисплей')
    processor_frequency = models.DecimalField(max_digits=2, decimal_places=2, verbose_name='Процессор частота GHz')
    ram = models.ForeignKey(RamProduct, on_delete=models.SET_NULL, verbose_name='Оперативная память', null=True)
    number_ram_slots = models.PositiveIntegerField(validators=[
        MaxValueValidator(8),
        MinValueValidator(1)
    ], verbose_name='Количество слотов памяти ОП')
    max_memory = models.PositiveIntegerField(validators=[
        MaxValueValidator(999),
        MinValueValidator(1)
    ], verbose_name='Максимальное количество ОП GB')
    free_slots = models.IntegerField(default=0, validators=[
        MaxValueValidator(8),
        MinValueValidator(0)
    ], verbose_name='Свободные слоты ОП')
    graphics_element = models.CharField(max_length=255)
    time_without_charge = models.CharField(max_length=255, verbose_name='Время работы батареи')

    class Meta:
        verbose_name = "Ноутбук"
        verbose_name_plural = "Ноутбуки"

    def __str__(self):
        return f'{self.category.name}: {self.title}'


class SmartphoneProduct(Product):
    diagonal = models.CharField(max_length=225, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Дисплей')
    screen = models.CharField(max_length=255, verbose_name='Разрешение экрана')
    processor_frequency = models.DecimalField(max_digits=2, decimal_places=2, verbose_name='Частота Процессора')
    ram = models.CharField(max_length=255, verbose_name='Ram info')
    accum_volume = models.IntegerField(validators=[
        MaxValueValidator(99999),
        MinValueValidator(1)
    ], verbose_name='Размер Аккамулятора')
    sd = models.BooleanField(default=False, verbose_name='Карта памяти')
    sd_volume_max = models.IntegerField(validators=[
        MaxValueValidator(999),
        MinValueValidator(1)
    ], verbose_name='Максимльный размер карты памяти Gb')
    main_cam = models.IntegerField(validators=[
        MaxValueValidator(999),
        MinValueValidator(1)
    ], verbose_name='Фронтальная камера Mp')
    front_cam = models.IntegerField(validators=[
        MaxValueValidator(999),
        MinValueValidator(1)
    ], verbose_name='Камера Mp')

    class Meta:
        verbose_name = "Сматрфон"
        verbose_name_plural = "Смартфоны"

    def __str__(self):
        return f'{self.category.name}: {self.title}'


class CartProduct(models.Model):
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE)
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
    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Итоговая цена')

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return str(self.id)
