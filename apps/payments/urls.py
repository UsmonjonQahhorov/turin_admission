from apps.payments import views
from django.urls import path, include


urlpatterns = [

    path("click/methods/", views.PaymentMethodListView.as_view(), name='methods'),
    path("payment/update/", views.ClickWebhook.as_view()),

    path("payment/initialize/click-payme", views.PaymentInitializeView.as_view(), name="click_payme_initializer")
]
