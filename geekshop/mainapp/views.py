from django.shortcuts import render
import json

links_menu = [
    {'href': 'products_all', 'name': 'все'},
    {'href': 'products_home', 'name': 'дом'},
    {'href': 'products_office', 'name': 'офис'},
    {'href': 'products_modern', 'name': 'модерн'},
    {'href': 'products_classic', 'name': 'классика'},
]

with open('/home/dimadat/PycharmProjects/django_basics/geekshop/mainapp/templates/mainapp/inc/inc_products_categories'
          '.json', 'r') as categories:
    products_categories = json.load(categories)


def main(request):
    content = {
        'title': 'главная',
    }
    return render(request, 'mainapp/index.html', content)


def products(request):
    content = {
        'title': "продукты",
        'links_menu': links_menu,
        'products_categories': products_categories,
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    content = {
        'title': 'контакты',
    }
    return render(request, 'mainapp/contact.html', content)
