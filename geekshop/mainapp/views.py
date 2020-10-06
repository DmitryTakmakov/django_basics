from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import ProductCategory, Product


def main(request):
    content = {
        'title': 'главная',
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()

    basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category=category)

        content = {
            'title': "продукты",
            'links_menu': links_menu,
            'category': category,
            'products': products_list,
            'basket': basket,
        }
        return render(request, 'mainapp/products_list.html', content)

    content = {
        'title': "продукты",
        'links_menu': links_menu,
        'basket': basket,
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    content = {
        'title': 'контакты',
    }
    return render(request, 'mainapp/contact.html', content)
