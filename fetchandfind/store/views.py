from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.

def home(request):
    template_n = loader.get_template('home.html')
    return HttpResponse(template_n.render())






