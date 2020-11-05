import urllib.request
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests
from django.conf import settings
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        api_url = urlunparse(('https',
                              'api.vk.com',
                              '/method/users.get',
                              None,
                              urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_200_orig')),
                                                    access_token=response['access_token'],
                                                    v='5.92')),
                              None
                              ))
        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]
        if data['sex']:
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

        if data['about']:
            user.shopuserprofile.about_me = data['about']

        if data['bdate']:
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

            age = timezone.now().date().year - bdate.year
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')
            user.age = age

        if data['photo_200_orig']:
            urllib.request.urlretrieve(data['photo_200_orig'], f'{settings.MEDIA_ROOT}/users_avatars/av_{user.pk}.jpg')
            user.avatar = f'users_avatars/av_{user.pk}.jpg'

        user.save()

    elif backend.name == 'google-oauth2':
        api_url = urlunparse(('https',
                              'people.googleapis.com/v1',
                              'people/me/',
                              None,
                              urlencode(OrderedDict(
                                  personFields=','.join(('emailAddresses', 'genders', 'names', 'birthdays')),
                                  key=settings.SOCIAL_AUTH_GOOGLE_API_KEY)),
                              None))

        resp = requests.get(api_url)
        # print(api_url)
        # print(response)
        # print(resp)
        # if resp.status_code != 200:
        #     return

        data = resp.json()
        if response['picture']:
            user.shopuserprofile.social_avatar = response['picture']

        user.save()

    else:
        return
