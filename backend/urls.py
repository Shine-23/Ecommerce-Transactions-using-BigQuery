"""
URL configuration for ecommerce_transaction_using_BigQuery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from api.views import CustomerListView, ProductListView, TransactionListView, ClickStreamListView, shutdown_service, metrics_view, log_request_view, secure_data
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.http import HttpResponseRedirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', CustomerListView.as_view(), name='customer'),
    path('products/', ProductListView.as_view(), name='product'),
    path('transactions/', TransactionListView.as_view(), name='transaction'),
    path('clickStream/', ClickStreamListView.as_view(), name='clickStream'),
    path('simulateFailure/', shutdown_service, name='simulate-failure'),
    path('metrics/', metrics_view, name='metrics'),
    path('log-request/', log_request_view, name='log-request'),
    path('secure-data/', secure_data, name='secure-data'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

