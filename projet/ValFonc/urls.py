from django.urls import path
from . import views as views
urlpatterns = [
    path('', views.index, name='index'),
    path('visu', views.visu, name='visu'),
    path('visuType', views.visuType, name='visuType'),
    path('visuReg', views.visuReg, name="visuReg"),
]