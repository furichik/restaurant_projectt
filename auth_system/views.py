from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterForm, LoginForm
from django.shortcuts import render
from restaurant.models import Order

def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'auth_system/profile.html', {
        'orders': orders
    })

def home(request):
    return render(request, "home.html")


class CustomLoginView(LoginView):
    template_name = "auth_system/login.html"
    authentication_form = LoginForm   
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = "home"   


class RegisterView(CreateView):
    template_name = "auth_system/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")