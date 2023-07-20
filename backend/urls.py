from django.urls import include, path

app_name = "backend"

urlpatterns = [
    path(r"", include("backend.auth.urls")),
    path(r"", include("backend.customer.urls")),
]
