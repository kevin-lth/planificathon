from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from . import lect_json

@csrf_exempt
def update_planning(request):
    planning_json = json.loads(request.body)
    print(planning_json)
    contraintes = lect_json.lecture(planning_json)
    result = json.dumps(contraintes)
    return HttpResponse(result, content_type='application/json')
