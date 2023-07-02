"""CoopCashInandOut URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from CashInOut import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.CashInOut, name='homepage'),
    path('profile/<str:profile_name>/', views.Customer_Profile, name='customer_profile'),
    path('', views.customer_input_form_view, name="customer-page"),
    path('records/daily', views.DailyRecords, name='records'),
    path('records/monthly', views.monthly_records, name='monthly'),
    path('records/yearly', views.yearly_records, name='yearly'),
    path('generate-pdf/', views.generate_pdf, name='generate-pdf'),
    path('generate-monthly-pdf/', views.generate_monthly_pdf, name='generate-monthly-pdf'),
    path('generate-annual-pdf/', views.generate_annual_pdf, name='generate-annual-pdf'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
