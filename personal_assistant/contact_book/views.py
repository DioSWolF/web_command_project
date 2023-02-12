from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q

from .forms import ContactForm
from .models import ContactBook


def checker(request):
    return render(
        request,
        "contact_book/checker.html",
        context={"msg": "Good news!!! It is working)"},
    )


@login_required(login_url='/login/')
def get_contact_book(request):
    contacts = ContactBook.objects.filter(owner=request.user).all()
    return render(
        request,
        "contact_book/main_contacts_book.html",
        context={"contacts": contacts},
    )


@login_required(login_url='/login/')
def create_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data_contact = form.save(commit=False)
            data_contact.owner = request.user
            data_contact.save()
            return redirect(to="contact_book:contacts_book")
        else:
            return render(
                request, "contact_book/create_contact.html", context={"form": form}
            )
    return render(
        request, "contact_book/create_contact.html", context={"form": ContactForm()}
    )


@login_required(login_url='/login/')
def datail(request, contact_id):
    contact = get_object_or_404(ContactBook, pk=contact_id, owner=request.user)
    return render(request, "contact_book/detail.html", context={"contact": contact})


@login_required(login_url='/login/')
def change_contact(request, contact_id):
    contact = get_object_or_404(ContactBook, pk=contact_id, owner=request.user)
    if request.method == "POST":
        form = ContactForm(request.POST)
        current_date = timezone.now()
        if form.is_valid():
            ContactBook.objects.filter(owner=request.user, pk=contact_id).update(
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                phone=request.POST["phone"],
                email=request.POST["email"],
                address=request.POST["address"],
                description=request.POST["description"],
                birthday=request.POST["birthday"],
                change_date=current_date,
            )
            return redirect(to="contact_book:contacts_book")
        else:
            return render(
                request, "contact_book/change_contact.html", context={"form": form}
            )
    try:
        birthday_str = contact.birthday.strftime("%Y-%m-%d")
    except:
        birthday_str = ""

    context = {"form": ContactForm(), "contact": contact, "birthday_str": birthday_str}
    return render(request, "contact_book/change_contact.html", context)


@login_required(login_url='/login/')
def find_by(request):
    contacts = ContactBook.objects.filter(owner=request.user)
    if request.method == "POST":

        find_by_method = request.POST["find_by"]
        search_value = (request.POST["search_value"])
        order_by_field = (request.POST["order_by_field"])

        if find_by_method == "first_name":
            contacts = ContactBook.objects.filter(owner=request.user, first_name__icontains=search_value)\
                .order_by(order_by_field)
        elif find_by_method == "last_name":
            contacts = ContactBook.objects.filter(owner=request.user, last_name__icontains=search_value)\
                .order_by(order_by_field)
        elif find_by_method == "phone":
            contacts = ContactBook.objects.filter(owner=request.user, phone__icontains=search_value)\
                .order_by(order_by_field)
        elif find_by_method == "email":
            contacts = ContactBook.objects.filter(owner=request.user, email__icontains=search_value)\
                .order_by(order_by_field)
        elif find_by_method == "address":
            contacts = ContactBook.objects.filter(owner=request.user, address__icontains=search_value)\
                .order_by(order_by_field)
        elif find_by_method == "description":
            contacts = ContactBook.objects.filter(owner=request.user, description__icontains=search_value)\
                .order_by(order_by_field)
        else:
            contacts = ContactBook.objects.filter(Q(first_name__icontains=search_value) |\
                                                  Q(last_name__icontains=search_value) |
                                                  Q(phone__icontains=search_value) |\
                                                  Q(email__icontains=search_value) |
                                                  Q(address__icontains=search_value) | \
                                                  Q(owner=request.user) | \
                                                  Q(description__icontains=search_value)).order_by(order_by_field)

    return render(request, "contact_book/find_by.html", context={"contacts": contacts})


@login_required(login_url='/login/')
def delete_contact(request, contact_id):
    if request.POST:
        ContactBook.objects.filter(owner=request.user, pk=contact_id).delete()
        return redirect(to="contact_book:contacts_book")
    return render(request, "contact_book/delete_contact.html")


@login_required(login_url='/login/')
def get_birthday_contacts(request):
    current_date = datetime.now().date()
    date_list = [current_date]
    date_birthday_list = []

    if request.method == "POST":
        delta_date = int(request.POST["days_to"])

        for i in range(delta_date + 1):
            _date = current_date + timedelta(days=i)
            date_list.append(_date)

        for i in date_list:
            context = ContactBook.objects.filter(owner=request.user, birthday__month=i.month, birthday__day=i.day)
            if context:
                date_birthday_list.append(context)

        return render(request, "contact_book/birthday_contacts.html", context={"contacts": date_birthday_list})

    for i in range(8):
        _date = current_date + timedelta(days=i)
        date_list.append(_date)

    for i in date_list:
        context = ContactBook.objects.filter(owner=request.user, birthday__month=i.month, birthday__day=i.day)

        if context:
            date_birthday_list.append(context)

    return render(request, "contact_book/birthday_contacts.html", context={"contacts": date_birthday_list})
