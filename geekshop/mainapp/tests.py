from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, Client

from mainapp.models import ProductCategory, Product


class MainappSmokeTest(TestCase):

    expected_success_code = 200

    def setUp(self):
        self.main_page = settings.DOMAIN_NAME + '/'
        self.contact_page = settings.DOMAIN_NAME + '/contact/'
        self.products_page = settings.DOMAIN_NAME + '/products/'
        self.products_all = settings.DOMAIN_NAME + '/products/category/0/'
        self.product_category_page = settings.DOMAIN_NAME + '/products/category/'
        self.product_page = settings.DOMAIN_NAME + '/products/product/'
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get(self.main_page)
        self.assertEqual(response.status_code, self.expected_success_code)

        response = self.client.get(self.contact_page)
        self.assertEqual(response.status_code, self.expected_success_code)

        response = self.client.get(self.products_page)
        self.assertEqual(response.status_code, self.expected_success_code)

        response = self.client.get(self.products_all)
        self.assertEqual(response.status_code, self.expected_success_code)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'{self.product_category_page}{category.pk}/')
            self.assertEqual(response.status_code, self.expected_success_code)

        for product in Product.objects.all():
            response = self.client.get(f'{self.product_page}{product.pk}/')
            self.assertEqual(response.status_code, self.expected_success_code)

    # def tearDown(self):
    #     call_command('sqlsequencereset', 'mainapp', 'authapp', 'orderapp', 'basketapp')
