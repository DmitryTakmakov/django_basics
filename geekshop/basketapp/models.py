from django.conf import settings
from django.db import models

from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='добавлено в корзину')

    @property
    def product_price(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = Basket.objects.filter(user=self.user).select_related()
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @property
    def total_cost(self):
        _items = Basket.objects.filter(user=self.user).select_related()
        _total_cost = sum(list(map(lambda x: x.product_price, _items)))
        return _total_cost

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user).order_by('product__category')

    @staticmethod
    def get_product(user, product):
        return Basket.objects.filter(user=user, product=product)

    @classmethod
    def get_products_quantity(cls, user):
        basket_items = cls.get_items(user)
        basket_items_dic = {}
        [basket_items_dic.update({item.product: item.quantity}) for item in basket_items]

        return basket_items_dic

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)
    
    # def save(self, *args, **kwargs):
    #     self.product.quantity -= self.quantity
    #     self.product.save()
    #     super(Basket, self).save(*args, **kwargs)
