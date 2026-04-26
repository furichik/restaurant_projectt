from django.urls import path
from .views import home, profile, CustomLoginView, CustomLogoutView, RegisterView

urlpatterns = [
    path('home/', home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
]