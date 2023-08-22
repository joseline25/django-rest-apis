from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

# a view to display all the available endpoints


def endpoints(request):
    data = ['/advocates', '/advocates/:username']
    return JsonResponse(data, safe=False)


# view for advocates

def advocate_list(request):
    # we want to return a list of name
    data = ['Joseline', 'Orliane', 'Aurelien', 'Clovis']
    return JsonResponse(data, safe=False)


# view for the details on an advocate from advocates

def advocate_details(request, username):
    data = [username]
    return JsonResponse(data, safe=False)
