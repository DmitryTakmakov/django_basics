from django.shortcuts import render
import json

from mainapp.models import ProductCategory


def main(request):
    content = {
        'title': 'главная',
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()
    content = {
        'title': "продукты",
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    content = {
        'title': 'контакты',
    }
    return render(request, 'mainapp/contact.html', content)
