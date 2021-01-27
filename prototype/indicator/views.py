from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from . import lect_json
from . import planning_donnees

@csrf_exempt
def update_planning(request):
    planning_json = json.loads(request.body)
    stuff = lect_json.lecture(planning_json)
    planning = planning_donnees.Planning(*stuff)
    result = json.dumps(planning)
    return HttpResponse(result, content_type='application/json')
