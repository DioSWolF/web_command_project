from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import ContactForm
from .models import ContactBook


def checker(request):
    return render(request, 'contact_book/checker.html', context={"msg": "Good news!!! It is working)"})


def get_contact_book(request):
    return render(request, 'contact_book/main_contacts_book.html', context={"contacts": ContactBook.objects.all()})


def create_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='contact_book:contacts_book')
        else:
            return render(request, 'contact_book/create_contact.html', context={"form": form})
    return render(request, 'contact_book/create_contact.html', context={"form": ContactForm()})


def datail(request, contact_id):
    contact = get_object_or_404(ContactBook, pk=contact_id)
    return render(request, 'contact_book/detail.html', context={'contact': contact})


def change_contact(request, contact_id):
    contact = get_object_or_404(ContactBook, pk=contact_id)
    if request.method == "POST":
        form = ContactForm(request.POST)
        current_date = timezone.now()
        if form.is_valid():
            ContactBook.objects.filter(pk=contact_id).update(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                phone=request.POST['phone'],
                email=request.POST['email'],
                address=request.POST['address'],
                description=request.POST['description'],
                birthday=request.POST['birthday'],
                change_date=current_date
            )

            return redirect(to='contact_book:contacts_book')
        else:
            return render(request, 'contact_book/change_contact.html', context={"form": form})
    birthday_str = contact.birthday.strftime('%Y-%m-%d')
    print('---------------------------------------------')
    print(birthday_str)
    print('---------------------------------------------')
    context = {"form": ContactForm(), 'contact': contact, 'birthday_str': birthday_str}
    return render(request, 'contact_book/change_contact.html', context)

    # contact = get_object_or_404(ContactBook, pk=contact_id)
    # return render(request, 'contact_book/detail.html', context={'contact': contact})



def find_by(request):
    return render(request, 'contact_book/find_by.html', context={"msg": "FIND BY"})


def delete_contact(request, contact_id):
    return render(request, 'contact_book/delete_contact.html', context={"msg": "DELETE"})


def get_birthday_contacts(request):
    return render(request, 'contact_book/birthday_contacts.html', context={"msg": "GET BIRTHDAY CONTACTS"})
