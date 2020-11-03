from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from basketapp.models import Basket
from orderapp.forms import OrderItemForm
from orderapp.models import Order, OrderItem


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'заказы'
        return context


class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_item = Basket.get_items(user=self.request.user)
            if len(basket_item):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_item))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_item[num].product
                    form.initial['quantity'] = basket_item[num].quantity
                basket_item.delete()
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        form.instance.user = self.request.user
        self.object = form.save()
        if orderitems.is_valid():
            orderitems.instance = self.object
            orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)

        data['orderitems'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        self.object = form.save()
        if orderitems.is_valid():
            orderitems.instance = self.object
            orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsUpdate, self).form_valid(form)


class OrderItemsDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('order:orders_list')


class OrderRead(DetailView):
    model = Order


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCESSING
    order.save()

    return HttpResponseRedirect(reverse('order:orders_list'))
