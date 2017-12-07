from django.shortcuts import render
from greenhouse.farm import query_farms
from greenhouse.farm import get_list_of_patterns
from greenhouse.farm import update_pattern_offset


def index(request):
    return render(request, 'greenhouse/index.html/', query_farms())


def greenhouse(request):
    return render(request, 'greenhouse/'+request.path, query_farms())


def settings(request):
    if request.POST:
        update_pattern_offset(request.POST['farm_url'], request.POST['pattern_offset'])
    farm_name = request.GET.get('farm')
    specific_farm = None
    if farm_name:
        specific_farm = [farm for farm in query_farms()['farms'] if farm['name'] == farm_name][0]
    return render(request, 'greenhouse/'+request.path[:-1]+'.html', {'farm': specific_farm,
                                                                     'climate_patterns': get_list_of_patterns()})
