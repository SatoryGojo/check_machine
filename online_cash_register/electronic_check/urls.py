from django.urls import path
from .views import CashRegisterView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("check_register/", CashRegisterView.as_view(), name='check_register'),
]
