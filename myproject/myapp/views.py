from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("<h1>Sound Fusion Limited</h1>")
def signup(request):
    pass
def login(request):
    pass
