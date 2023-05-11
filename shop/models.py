from django.contrib.auth.models import User
from django.db import models


class Vendors(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(null=True)


class Customers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30)  # Try a first positional argument
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    address = models.CharField(max_length=255)


class Products(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="photos/%Y/%m/%d/")
    units_in_stock = models.IntegerField(default=0)
    categories = models.ManyToManyField('Categories', through='ProductsCategories')
    vendor = models.ForeignKey(Vendors, on_delete=models.PROTECT)

    def add_to_stock(self, value):
        self.units_in_stock += value
        self.save()

    def take_from_stock(self, value):
        if self.units_in_stock < value:
            pass
        else:
            self.units_in_stock -= value


class Categories(models.Model):
    name = models.CharField(max_length=30)


class Orders(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.PROTECT)
    time_create = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Products, through='OrdersProducts')


class ProductsCategories(models.Model):
    product = models.ForeignKey(Products, on_delete=models.PROTECT)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)


class OrdersProducts(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.PROTECT)
    product = models.ForeignKey(Products, on_delete=models.PROTECT)
    _amount = models.IntegerField(default=1, db_column='amount')

    # Метод возвращает полную стоимость в заказе
    def get_total_price(self):
        product_price = self.product.price
        return self.amount * product_price

    @property  # Геттер для поля amount
    def amount(self):
        return self._amount

    @amount.setter  # Сеттер для поля amount
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()
