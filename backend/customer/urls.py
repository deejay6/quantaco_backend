from django.urls import path

from .views import CustomerView

app_name = "backend.customer"
urlpatterns = [
    path("customer", CustomerView.as_view()),
]
