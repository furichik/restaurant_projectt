from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_system.urls')),
    path('', include('restaurant.urls')),
]