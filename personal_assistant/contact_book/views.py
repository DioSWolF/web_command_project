from django.shortcuts import render


def checker(request):
    return render(request, 'contact_book/checker.html', context={"msg": "Good news!!! It is working)"})

