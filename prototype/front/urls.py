from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='front_index'),
    path('update_planning', views.update_planning, name='update')
]
