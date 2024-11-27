from django.urls import path

from . import views


app_name = "api"

urlpatterns = [
    path("wallets/<uuid:wallet_uuid>/",
         views.ShowWalletInfoAPI.as_view(),
         name="show_balance"),
    path("wallets/<uuid:wallet_uuid>/operation/",
         views.ProceedWalletOperationAPI.as_view(),
         name="wallet_operation")
]
