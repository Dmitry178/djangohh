from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from .forms import RegistrationForm
from django.views.generic import CreateView, DetailView
from .models import HhUser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse


# Create your views here.
class UserLoginView(LoginView):
    template_name = 'userapp/login.html'


class UserCreateView(CreateView):
    model = HhUser
    template_name = 'userapp/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login')


class UserDetailView(DetailView):
    template_name = 'userapp/profile.html'
    model = HhUser


def update_token(request):
    user = request.user
    # if user.auth_token:  - не работает, если нет токена
    try:
        user.auth_token.delete()
    except:
        pass

    Token.objects.create(user=user)

    return HttpResponseRedirect(reverse('users:profile', kwargs={'pk': user.pk}))


def update_token_ajax(request):
    user = request.user
    try:
        user.auth_token.delete()
    except:
        pass

    token = Token.objects.create(user=user)

    return JsonResponse({'key': token.key})
