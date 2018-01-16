from django.shortcuts import render
from django.http import HttpResponse
from greenhouse.farm import query_farms
from greenhouse.farm import get_list_of_patterns
from greenhouse.farm import update_farm


def index(request):
    return render(request, 'greenhouse/index.html/', query_farms())


def greenhouse(request):
    try:
        return render(request, 'greenhouse/'+request.path, query_farms())
    except:
        return HttpResponse('Page not found', 404)


def favicon(request):
    with open('greenhouse/static/favicon.ico', "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")


def settings(request):
    if request.POST:
        if update_farm(request.POST):
            return HttpResponse('Changes Accepted', 200)
        else:
            return HttpResponse('Bad Data', 400)
    farm_name = request.GET.get('farm')
    specific_farm = None
    if farm_name:
        specific_farm = [farm for farm in query_farms()['farms'] if farm['name'] == farm_name][0]
    return render(request, 'greenhouse/'+request.path[:-1]+'.html', {'farm': specific_farm,
                                                                     'climate_patterns': get_list_of_patterns()})
