from django.urls import path
from . import views

app_name = "contact_book"

urlpatterns = [
    path("checker/", views.checker, name="checker"),
    path("", views.get_contact_book, name="contacts_book"),
    path("create/", views.create_contact, name="create_contact"),
    path("change/<int:contact_id>", views.change_contact, name="change_contact"),
    path("find/", views.find_by, name="find_contact"),
    path("delete/<int:contact_id>", views.delete_contact, name="delete_contact"),
    path("birthday/", views.get_birthday_contacts, name="get_birthday_contacts"),
    path("detail/<int:contact_id>", views.datail, name="detail"),
]
