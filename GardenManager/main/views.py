

import os

from django.http import HttpResponseRedirect
from django.shortcuts import render
from models import User



def get_default_context (user=None):
  context = {
    "user": user or User (),
    "title": "Garden Project",
    "error": "There are not any error!!! lel",
    "google_api_key": os.environ.get ("GOOGLE_MAPS_API_KEY", ""),
  }
  return context


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
