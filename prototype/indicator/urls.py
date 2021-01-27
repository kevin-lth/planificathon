from django.urls import path

from . import views

urlpatterns = [
    path('update_planning', views.update_planning, name='indicator_update')
]
