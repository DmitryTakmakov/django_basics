from django.conf import settings
from django.test import TestCase, Client

from authapp.models import ShopUser


class TestUserAuthTestCase(TestCase):
    expected_success_code = 200
    found_status_code = 302

    def setUp(self):
        self.client = Client()
        self.main_page = settings.DOMAIN_NAME + '/'
        self.login_page = settings.DOMAIN_NAME + '/auth/login/'
        self.logout_page = settings.DOMAIN_NAME + '/auth/logout/'
        self.register_page = settings.DOMAIN_NAME + '/auth/register/'
        self.basket_page = settings.DOMAIN_NAME + '/basket/'
        self.superuser = ShopUser.objects.create_superuser('django2', 'admin@geek.shop', 'geekbrains')
        self.user = ShopUser.objects.create_user('test_django_dummy', 'test@geek.shop', 'geekbrains')
        self.user_with__first_nam = ShopUser.objects.create_user('another_django_dummy', 'test2@geek.shop',
                                                                 'geekbrains', first_name='Dummy')

    def test_user_login(self):
        response = self.client.get(self.main_page)
        self.assertEqual(response.status_code, self.expected_success_code)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'главная')
        self.assertNotIn('Пользователь', response.content.decode())

        self.client.login(username='test_django_dummy', password='geekbrains')

        response = self.client.get(self.login_page)
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        response = self.client.get(self.main_page)
        self.assertIn('Пользователь', response.content.decode())
        self.assertEqual(response.context['user'], self.user)

    def test_basket_login_redirect(self):
        response = self.client.get(self.basket_page)
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, self.found_status_code)

        self.client.login(username='test_django_dummy', password='geekbrains')

        response = self.client.get(self.basket_page)
        self.assertEqual(response.status_code, self.expected_success_code)
        self.assertEqual(list(response.context['basket']), [])
        self.assertEqual(response.request['PATH_INFO'], '/basket/')
        self.assertIn('Ваша корзина, Пользователь', response.content.decode())

    def test_user_logout(self):
        self.client.login(username='test_django_dummy', password='geekbrains')

        response = self.client.get(self.login_page)
        self.assertEqual(response.status_code, self.expected_success_code)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get(self.logout_page)
        self.assertEqual(response.status_code, self.found_status_code)

        response = self.client.get(self.main_page)
        self.assertEqual(response.status_code, self.expected_success_code)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_user_register(self):
        response = self.client.get(self.register_page)
        self.assertEqual(response.status_code, self.expected_success_code)
        self.assertEqual(response.context['title'], 'регистрация')

        new_user_data = {
            'username': 'register_dummy',
            'first_name': 'Dummy',
            'password1': 'geekbrains1',
            'password2': 'geekbrains1',
            'email': 'dummy@geek.shop',
            'avatar': 'dummy_avatar.jpg',
            'age': '30'
        }

        response = self.client.post(self.register_page, data=new_user_data)
        self.assertEqual(response.status_code, self.found_status_code)
        new_user = ShopUser.objects.get(username=new_user_data['username'])

        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{new_user_data['email']}/{new_user.activation_key}"
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.expected_success_code)

        self.client.login(username=new_user_data['username'], password=new_user_data['password1'])
        response = self.client.get(self.login_page)
        self.assertEqual(response.status_code, self.expected_success_code)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get(self.main_page)
        self.assertContains(response, text=new_user_data['first_name'], status_code=self.expected_success_code)

    def test_user_invalid_password(self):
        new_user_data = {
            'username': 'register_dummy',
            'first_name': 'Dummy',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'dummy@geek.shop',
            'avatar': 'dummy_avatar.jpg',
            'age': '30'
        }
        response = self.client.post(self.register_page, data=new_user_data)
        self.assertEqual(response.status_code, self.expected_success_code)
        self.assertFormError(response, 'form', 'password1',
                             'В пароле должны быть цифры или символы "!?$*%^&#@".')

    def test_user_invalid_age(self):
        new_user_data = {
            'username': 'register_dummy',
            'first_name': 'Dummy',
            'password1': 'geekbrains1',
            'password2': 'geekbrains1',
            'email': 'dummy@geek.shop',
            'avatar': 'dummy_avatar.jpg',
            'age': '17'
        }
        response = self.client.post(self.register_page, data=new_user_data)
        self.assertEqual(response.status_code, self.expected_success_code)
        self.assertFormError(response, 'form', 'age',
                             'Вам нет 18 лет!')
