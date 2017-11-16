from django.shortcuts import render


def index(request):
    return render(request, 'greenhouse/index.html'+request.get_full_path())


def greenhouse(request):
    return render(request, 'greenhouse/'+request.get_full_path())
