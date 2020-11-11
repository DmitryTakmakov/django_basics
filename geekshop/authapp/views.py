from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from authapp.models import ShopUser


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            print(f'Error activating user: {email}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(e.args)
        return HttpResponseRedirect(reverse('main'))


def send_verification_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    subject = f'Подтверждение аккаунта пользователя {user.username}'

    message_text = f'Здравствуйте, {user.username}!\nДля подтверждения вашего аккаунта перейдите по ссылке:\n ' \
                   f'{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(subject, message_text, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST)

    next_url = request.GET.get('next', '')

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('main'))

    content = {
        'title': title,
        'login_form': login_form,
        'next': next_url,
    }
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


class UserRegisterView(CreateView):
    model = ShopUser
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('authapp:login')
    form_class = ShopUserRegisterForm

    def get_context_data(self, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        context['title'] = 'регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        if send_verification_email(user):
            print(f'Sending email to {user.email}: Success')
        else:
            print(f'Sending email to {user.email}: Error')
        user.save()

        return HttpResponseRedirect(self.success_url)


class UserEditView(UpdateView):
    model = ShopUser
    template_name = 'authapp/edit.html'
    success_url = reverse_lazy('main')
    fields = []

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(UpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserEditView, self).get_context_data(**kwargs)
        context['title'] = 'редактирование'
        if self.request.POST:
            context['form'] = ShopUserEditForm(self.request.POST, self.request.FILES, instance=self.object)
            context['profile_form'] = ShopUserProfileEditForm(self.request.POST, instance=self.object.shopuserprofile)
            print(context['form'])  # я не знаю почему, но сохранение файлов работает только когда здесь есть принт))
        else:
            context['form'] = ShopUserEditForm(instance=self.object)
            context['profile_form'] = ShopUserProfileEditForm(instance=self.object.shopuserprofile)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        profile_form = context['profile_form']

        self.object = form.save()
        if profile_form.is_valid():
            profile_form.instance = self.object
            profile_form.save()

        return super(UserEditView, self).form_valid(form)
