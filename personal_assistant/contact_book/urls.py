from django.urls import path
from . import views

app_name = "contact_book"

urlpatterns = [
    path('checker/', views.checker, name="checker"),
]
