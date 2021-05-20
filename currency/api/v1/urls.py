from django.urls import path

from currency.api.v1.views import CurrencyConverterAPIView, UserLoginAPIView

app_name = "currency"

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name="login"),
    path("currency-converter/", CurrencyConverterAPIView.as_view(), name="currency_converter"),
]
