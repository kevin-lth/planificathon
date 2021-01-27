from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='converter_index'),
    path('xlsx_to_json', views.xlsx_to_json, name='converter_xlsx_to_json'),
    path('json_to_xlsx', views.json_to_xlsx, name='converter_json_to_xlsx'),
]
