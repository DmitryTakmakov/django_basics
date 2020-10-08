import random

from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import ProductCategory, Product


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []


def get_hot_product():
    products_list = Product.objects.all()
    return random.sample(list(products_list), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category_id=hot_product.category_id).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    latest_products = Product.objects.all()[:3]
    content = {
        'title': 'главная',
        'latest_products': latest_products,
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk).order_by('price')

        content = {
            'title': "продукты",
            'links_menu': links_menu,
            'category': category,
            'products': products_list,
            'basket': get_basket(request.user),
        }
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': "продукты",
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    content = {
        'title': 'контакты',
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/contact.html', content)


def not_found(request, exception):
    products = Product.objects.all()[:3]
    content = {
        'products': products
    }
    return render(request, 'mainapp/404.html', content)


def product(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    title = product_item.name
    content = {
        'title': title,
        'product': product_item,
        'basket': get_basket(request.user),
        'links_menu': ProductCategory.objects.all(),
        'same_products': get_same_products(product_item),
    }

    return render(request, 'mainapp/product_page.html', content)
