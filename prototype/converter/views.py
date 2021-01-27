from django.http import HttpResponse, FileResponse
import json

from django.core.files.temp import NamedTemporaryFile
from django import forms

from . import xlsx_converter

class XLSXToJSONForm(forms.Form):
    sheet = forms.CharField(max_length=50)
    file = forms.FileField()

def index(request):
    return HttpResponse("Hello world. This is the converter !")
    
def __handle_xlsx_file__(file, sheet, then):
    with NamedTemporaryFile(delete=True, suffix=".xlsx") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        return then(destination.name, sheet)
        
def __send_xlsx_file__(filename):
        return FileResponse(open(filename, 'rb')) 

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def xlsx_to_json(request):
    if request.method == 'POST':
        form = XLSXToJSONForm(request.POST, request.FILES)
        if form.is_valid():
            result = __handle_xlsx_file__(request.FILES["file"], request.POST["sheet"], xlsx_converter.xlsx_to_dict)
            json_result = json.dumps(result)
            return HttpResponse(json_result, content_type='application/json')
            
@csrf_exempt
def json_to_xlsx(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        return xlsx_converter.dict_to_xlsx(data, __send_xlsx_file__)
