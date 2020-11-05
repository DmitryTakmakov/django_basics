from django.urls import path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.UserRegisterView.as_view(), name='register'),
    path('edit/<pk>/', authapp.UserEditView.as_view(), name='edit'),
    path('verify/<email>/<activation_key>', authapp.verify, name='verify'),
]
