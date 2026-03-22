from django.urls import path
from . import views

app_name = 'auth_system'
urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='Login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]
