import json
import os
import random

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from mainapp.models import ProductCategory, Product

JSON_FILE_PATH = os.path.join(settings.BASE_DIR, 'mainapp/json')
with open(os.path.join(JSON_FILE_PATH, 'contact__locations.json'), 'r', encoding='utf-8') as f:
    contact_locations = json.load(f)


def get_hot_product():
    products_list = Product.objects.all()
    return random.sample(list(products_list), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category_id=hot_product.category_id).exclude(pk=hot_product.pk)[:3]
    return same_products


class IndexPageView(TemplateView):
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context['title'] = 'главная'
        context['latest_products'] = Product.objects.all()[:3]
        return context


def products(request, pk=None, page=1):
    title = 'продукты'
    links_menu = ProductCategory.objects.filter(is_active=True)

    if pk is not None:
        if pk == 0:
            category = {
                'pk': 0,
                'name': 'все',
            }
            products_list = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')

        paginator = Paginator(products_list, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
        }
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': "продукты",
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/products.html', content)


class ContactPageView(TemplateView):
    template_name = 'mainapp/contact.html'

    def get_context_data(self, **kwargs):
        context = super(ContactPageView, self).get_context_data(**kwargs)
        context['title'] = 'контакты'
        context['locations'] = contact_locations
        return context


def not_found(request, exception):
    products = Product.objects.all()[:3]
    content = {
        'products': products
    }
    return render(request, 'mainapp/404.html', content)


def product(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    links_menu = ProductCategory.objects.filter(is_active=True)
    title = product_item.name
    content = {
        'title': title,
        'product': product_item,
        'links_menu': links_menu,
        'same_products': get_same_products(product_item),
    }

    return render(request, 'mainapp/product_page.html', content)
