from apps.payments import views
from django.urls import path, include


urlpatterns = [

    path("click/methods/", views.PaymentMethodListView.as_view(), name='methods'),
    path("payment/click/", views.ClickWebhook.as_view()),

    path("click/initialize/", views.PaymentInitializeView.as_view(), name="click_initializer")
]
