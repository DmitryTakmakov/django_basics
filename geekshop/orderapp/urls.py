from django.urls import path
import orderapp.views as orderapp

app_name = 'orderapp'

urlpatterns = [
    path('', orderapp.OrderList.as_view(), name='orders_list'),
    path('create/', orderapp.OrderItemsCreate.as_view(), name='order_create'),
    path('read/<pk>/', orderapp.OrderRead.as_view(), name='order_read'),
    path('update/<pk>', orderapp.OrderItemsUpdate.as_view(), name='order_update'),
    path('delete/<pk>/', orderapp.OrderItemsDelete.as_view(), name='order_delete'),
    path('forming/<pk>/', orderapp.order_forming_complete, name='order_forming_complete'),
    path('processing/<pk>/', orderapp.order_processing_imitation, name='order_processing_imitation'),
    path('product/<pk>/price/', orderapp.get_product_price)
]
