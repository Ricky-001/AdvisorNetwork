from django.urls import path, include
from rest_framework.authtoken import views as vws
from . import views
from .models import Advisor, User

urlpatterns = [
    path('api-token-auth/', vws.obtain_auth_token),
    path('', views.home),    
    path('admin/', views.AdminHome),
    path('user/', views.UserHome),
    path('admin/advisor/', views.AddAdvisor),
    path('user/register/', views.UserRegister),
    path('user/login/', views.UserLogin),
    path('user/<int:uid>/', views.AuthUser),
    path('user/<int:uid>/advisor/', views.ViewAll),
    path('user/<int:uid>/advisor/<int:aid>/', views.BookAdvisor),
    path('user/<int:uid>/advisor/booking/', views.ViewBookings),
]
