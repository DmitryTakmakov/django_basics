from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import mainapp.views as mainapp

urlpatterns = [
    path('', mainapp.IndexPageView.as_view(), name='main'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('contact/', mainapp.ContactPageView.as_view(), name='contact'),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('admin/', include('adminapp.urls', namespace='adminapp')),
    path('', include('social_django.urls', namespace='social')),
    path('order/', include('orderapp.urls', namespace='order')),
]

handler404 = mainapp.not_found

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
