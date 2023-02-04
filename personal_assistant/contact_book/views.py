from django.shortcuts import render


def checker(request):
    return render(request, 'contact_book/checker.html', context={"msg": "Good news!!! It is working)"})


def get_contact_book(request):
    return render(request, 'contact_book/main_contacts_book.html', context={"msg": "MAIN"})


def create_contact(request):
    return render(request, 'contact_book/create_contact.html', context={"msg": "CREATE"})


def change_contact(request):
    return render(request, 'contact_book/change_contact.html', context={"msg": "CHANGE"})


def find_by(request):
    return render(request, 'contact_book/find_by.html', context={"msg": "FIND BY"})


def delete_contact(request):
    return render(request, 'contact_book/delete_contact.html', context={"msg": "DELETE"})


def get_birthday_contacts(request):
    return render(request, 'contact_book/birthday_contacts.html', context={"msg": "GET BIRTHDAY CONTACTS"})
