import json
import os
import random

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from mainapp.models import ProductCategory, Product

JSON_FILE_PATH = os.path.join(settings.BASE_DIR, 'mainapp/json')
with open(os.path.join(JSON_FILE_PATH, 'contact__locations.json'), 'r', encoding='utf-8') as f:
    contact_locations = json.load(f)


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    products_list = get_products()
    try:
        return random.sample(list(products_list), 1)[0]
    except ValueError as e:
        print(f'error! {e}')
        dummy_cat = ProductCategory.objects.create(id=1, name='dummy')
        return Product.objects.create(pk=0, category_id=dummy_cat.id, name='dummy_product')


def get_same_products(hot_product):
    same_products = Product.objects.filter(category_id=hot_product.category_id).exclude(
        pk=hot_product.pk).select_related()[:3]
    return same_products


class IndexPageView(TemplateView):
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context['title'] = 'главная'
        context['latest_products'] = get_products()[:3]
        return context


# @cache_page(3600)
def products(request, pk=None, page=1):
    title = 'продукты'
    links_menu = get_links_menu()

    if pk is not None:
        if pk == 0:
            category = {
                'pk': 0,
                'name': 'все',
            }
            products_list = get_products_ordered_by_price()
        else:
            category = get_category(pk)
            products_list = get_products_in_category_ordered_by_price(pk)

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
        if settings.LOW_CACHE:
            key = 'contact_locations'
            locations = cache.get(key)
            if locations is None:
                context['locations'] = contact_locations
                cache.set(key, locations)
        else:
            context['locations'] = contact_locations
        return context


def not_found(request, exception):
    products = Product.objects.all()[:3]
    content = {
        'products': products
    }
    return render(request, 'mainapp/404.html', content)


def product(request, pk):
    product_item = get_product(pk)
    links_menu = get_links_menu()
    title = product_item.name
    content = {
        'title': title,
        'product': product_item,
        'links_menu': links_menu,
        'same_products': get_same_products(product_item),
    }

    return render(request, 'mainapp/product_page.html', content)
