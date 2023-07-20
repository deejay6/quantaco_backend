from django.urls import path

from .views import LoginView, LogoutView, RegisterView

app_name = "backend.auth"
urlpatterns = [
    path("auth/register", RegisterView.as_view()),
    path("auth/login", LoginView.as_view()),
    path("auth/logout", LogoutView.as_view()),
]
