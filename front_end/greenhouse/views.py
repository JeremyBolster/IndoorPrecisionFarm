from django.shortcuts import render
from greenhouse.farm import query_farms


def index(request):
    return render(request, 'greenhouse/index.html'+request.get_full_path(), query_farms())


def greenhouse(request):
    return render(request, 'greenhouse/'+request.get_full_path())
