"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('mentor/login/', views.mentor_login, name='mentor_login'),
    path('register/', views.student_register, name='student_register'),
    path('login/', views.student_login, name='student_login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('mentors/', views.mentor_list, name='mentor_list'),
    path('mentors/<int:mentor_id>/', views.mentor_detail, name='mentor_detail'),
    path('mentor/availability/', views.mentor_availability, name='mentor_availability'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
    path('payment/confirm/<int:booking_id>/', views.confirm_payment, name='confirm_payment'),

]


