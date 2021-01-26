from django.http import HttpResponse, JsonResponse

def index(request):
    return HttpResponse("Hello world. This is the converter !")
