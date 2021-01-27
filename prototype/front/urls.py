from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='front_index'),
    path('planning_json/', views.planning_as_json, name='planning'),
    path('agents_json/', views.agents_as_json, name='agents'),
    path('update_planning', views.update_planning, name='update')
]
