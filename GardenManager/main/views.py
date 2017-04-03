from django.shortcuts import render

# Create your views here.

def root (request):
  title = "Garden Project"
  return render (request, "creation_plan.html")