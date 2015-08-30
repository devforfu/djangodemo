from django.shortcuts import render, redirect
from django.http import HttpResponse


def home_page(request):
    if request.is_ajax() or request.method == 'POST':
        return HttpResponse("AJAX request handled")

    return render(request, 'index.html')
