from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Bonjour, bienvenue sur les visuels fonciers français")