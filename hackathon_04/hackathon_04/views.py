from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'search.html')


def submit(request):
    # return render(request, 'test.html')
    return HttpResponse(request.POST.get('search'))
