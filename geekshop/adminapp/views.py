from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи / создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserRegisterForm()

    content = {
        'title': title,
        'update_form': user_form,
    }

    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'пользователи'

    users_list = ShopUser.objects.all()

    content = {
        'title': title,
        'objects': users_list,
    }

    return render(request, 'adminapp/users.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи / редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_update', args=[edit_user.pk]))
    else:
        user_form = ShopUserAdminEditForm(instance=edit_user)

    content = {
        'title': title,
        'update_form': user_form,
    }

    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователи / удаление'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        if edit_user.is_active:
            edit_user.is_active = False
        else:
            edit_user.is_active = True
        edit_user.save()
        return HttpResponseRedirect(reverse('adminapp:users'))

    content = {
        'title': title,
        'user_to_delete': edit_user,
    }

    return render(request, 'adminapp/user_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'категории / создание'

    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        category_form = ProductCategoryEditForm()

    content = {
        'title': title,
        'update_form': category_form,
    }

    return render(request, 'adminapp/category_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'категории'

    categories_list = ProductCategory.objects.all()

    content = {
        'title': title,
        'objects': categories_list,
    }

    return render(request, 'adminapp/categories.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'категории / редактирование'

    edit_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('adminapp:category_update', args=[edit_category.pk]))
    else:
        category_form = ProductCategoryEditForm(instance=edit_category)

    content = {
        'title': title,
        'update_form': category_form,
    }

    return render(request, 'adminapp/category_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = 'категории / удаление'

    edit_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        if edit_category.is_active:
            edit_category.is_active = False
        else:
            edit_category.is_active = True
        edit_category.save()
        return HttpResponseRedirect(reverse('adminapp:categories'))

    content = {
        'title': title,
        'category_to_delete': edit_category,
    }

    return render(request, 'adminapp/category_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'продукты / создание'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('adminapp:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    content = {
        'title': title,
        'update_form': product_form,
        'category': category
    }

    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'продукты'

    category_item = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category=category_item)

    content = {
        'title': title,
        'objects': products_list,
        'category': category_item,
    }

    return render(request, 'adminapp/products.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    title = 'продукты / детализация'

    product = get_object_or_404(Product, pk=pk)

    content = {
        'title': title,
        'object': product,
    }

    return render(request, 'adminapp/product_read.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукты / редактирование'

    edit_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('adminapp:product_update', args=[edit_product.pk]))
    else:
        product_form = ProductEditForm(instance=edit_product)

    content = {
        'title': title,
        'update_form': product_form,
        'category': edit_product.category,
    }

    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукты / удаление'

    edit_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        if edit_product.is_active:
            edit_product.is_active = False
        else:
            edit_product.is_active = True
        edit_product.save()
        return HttpResponseRedirect(reverse('adminapp:products', args=[edit_product.category.pk]))

    content = {
        'title': title,
        'product_to_delete': edit_product,
    }

    return render(request, 'adminapp/product_delete.html', content)
