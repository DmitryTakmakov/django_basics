from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='index'),
    path('<pk>/', mainapp.products, name='category'),
]
