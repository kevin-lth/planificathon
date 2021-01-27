from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json

def index(request):
    return render(request, "index.html")

