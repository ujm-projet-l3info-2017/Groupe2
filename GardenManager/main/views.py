

from django.http import HttpResponseRedirect
from django.shortcuts import render
from models import User



def get_default_context (user=None):
  return {
    "user": user or User (),
    "title": "Garden Project",
  }


def root (request, user=None):
  return render (request, "root.html", context=get_default_context (user))


def login (request):
  request.session["_old_post"] = request.POST
  return HttpResponseRedirect ("/")


def register (request):
  request.session["_old_post"] = request.POST
  return HttpResponseRedirect ("/")


def logout (request):
  request.session["_old_post"] = request.POST
  return HttpResponseRedirect ("/")
