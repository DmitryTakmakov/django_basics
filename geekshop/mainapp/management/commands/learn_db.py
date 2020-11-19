from datetime import timedelta

from django.core.management import BaseCommand
from django.db import connection
from django.db.models import Q, F, When, Case, IntegerField, DecimalField

from adminapp.views import db_profile_by_type
from mainapp.models import Product
from orderapp.models import OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        # test_products = Product.objects.filter(Q(category__name='офис') | Q(category__name='модерн')).select_related()
        #
        # print(len(test_products))
        # print(test_products)
        #
        # db_profile_by_type('learn_db', '', connection.queries)

        OFFER_1 = 1
        OFFER_2 = 2
        OFFER_EXPIRED = 3

        offer_1__time_delta = timedelta(hours=12)
        offer_2__time_delta = timedelta(days=1)

        offer_1__discount = 0.3
        offer_2__discount = 0.15
        offer_expired__discount = 0.05

        offer_1__condition = Q(order__updated__lte=F('order__created') + offer_1__time_delta)
        offer_2__condition = Q(order__updated__gt=F('order__created') + offer_1__time_delta) & Q(
            order__updated__lte=F('order__created') + offer_2__time_delta)
        offer_expired__condition = Q(order__updated__gt=F('order__created') + offer_2__time_delta)

        offer_1__order = When(offer_1__condition, then=OFFER_1)
        offer_2__order = When(offer_2__condition, then=OFFER_2)
        offer_expired__order = When(offer_expired__condition, then=OFFER_EXPIRED)

        offer_1__price = When(offer_1__condition, then=F('product__price') * F('quantity') * offer_1__discount)
        offer_2__price = When(offer_2__condition, then=F('product__price') * F('quantity') * offer_2__discount)
        offer_expired__price = When(offer_expired__condition,
                                    then=F('product__price') * F('quantity') * offer_expired__discount)

        test_orders = OrderItem.objects.annotate(
            offer_order=Case(
                offer_1__order,
                offer_2__order,
                offer_expired__order,
                output_field=IntegerField(),
            )).annotate(
            total_price=Case(
                offer_1__price,
                offer_2__price,
                offer_expired__price,
                output_field=DecimalField(),
            )).order_by('offer_order', 'total_price').select_related()

        for orderitem in test_orders:
            print(f'{orderitem.offer_order:2}: заказ №{orderitem.pk:3}: '
                  f'{orderitem.product.name:15}: скидка '
                  f'{abs(orderitem.total_price):6.2f} руб. | '
                  f'{orderitem.order.updated - orderitem.order.created}')
