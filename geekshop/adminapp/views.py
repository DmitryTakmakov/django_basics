from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from django.db.models import F
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm, OrderEditForm, \
    OrderItemEditForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from orderapp.models import Order, OrderItem


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('adminapp:users')
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи / создание'
        return context


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи'
        return context


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('adminapp:users')
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи / редактирование'
        return context


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('adminapp:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи / удаление'
        return context


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:categories')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории / создание'
        return context


class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории'
        return context


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:categories')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории / редактирование'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)
        return super().form_valid(form)


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории / удаление'
        return context


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('adminapp:products')
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты / создание'
        category_pk = self.kwargs.get('pk', None)
        if category_pk is not None:
            context['category'] = get_object_or_404(ProductCategory, pk=category_pk)
            context['form']['category'].initial = get_object_or_404(ProductCategory, pk=category_pk)
            return context

    def get_success_url(self):
        category_pk = self.object.category.pk
        return reverse_lazy('adminapp:products', kwargs={'pk': category_pk})


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты'
        category_pk = self.kwargs.get('pk', None)
        if category_pk is not None:
            context['category'] = get_object_or_404(ProductCategory, pk=category_pk)
            return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_pk = self.kwargs.get('pk', None)
        if category_pk is not None:
            queryset = Product.objects.filter(category_id=category_pk).select_related()
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт / подробнее'
        return context


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('adminapp:products')
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты / редактирование'
        category_pk = self.object.category.pk
        if category_pk is not None:
            context['category'] = get_object_or_404(ProductCategory, pk=category_pk)
            return context

    def get_success_url(self):
        category_pk = self.object.category.pk
        return reverse_lazy('adminapp:products', kwargs={'pk': category_pk})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('adminapp:products')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты / редактирование'
        category_pk = self.object.category.pk
        if category_pk is not None:
            context['category'] = get_object_or_404(ProductCategory, pk=category_pk)
            return context

    def get_success_url(self):
        category_pk = self.object.category.pk
        return reverse_lazy('adminapp:products', kwargs={'pk': category_pk})


class OrderListView(ListView):
    model = Order
    template_name = 'adminapp/orders.html'
    paginate_by = 5

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'заказы'
        return context

    def get_queryset(self):
        return super(OrderListView, self).get_queryset().exclude(status=Order.CANCELLED).select_related()


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'adminapp/order_update.html'
    success_url = reverse_lazy('admin:orders')
    form_class = OrderEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'заказы / редактирование'
        print(context)
        return context


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'adminapp/order_delete.html'
    success_url = reverse_lazy('admin:orders')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'заказы / удаление'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class OrderDetailView(UpdateView):
    model = Order
    template_name = 'adminapp/order_read.html'
    success_url = reverse_lazy('admin:orders')
    form_class = OrderItemEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemEditForm, extra=1)
        if self.request.POST:
            context['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            queryset = self.object.orderitems.select_related()
            formset = OrderFormSet(instance=self.object, queryset=queryset)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
            context['orderitems'] = formset
        context['title'] = f'заказы / детали заказа №{self.object.id}'
        return context


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
