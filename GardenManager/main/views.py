

import os

from django.http import HttpResponseRedirect
from django.shortcuts import render
from models import User
from urllib2 import build_opener
from urllib2 import Request
from json import load





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

class Weather ():
  
  def __init__ (self, latitude, longitude):
    request_url = self.get_request_url(latitude, longitude)
    json_output = self.get_request_output(request_url)
    self.__dict__  = load(json_output)
    print self.list[0]["humidity"]
    
  def get_owm_api_key (self):
    return '2d5dd571dc377d57fd57c3b30cea7335'

  def get_request_url (self, latitude, longitude):
    return 'http://api.openweathermap.org/data/2.5/forecast/daily?' +\
     'lat=' + str(longitude) +\
     '&lon=' + str(latitude) +\
     '&mode=json' +\
     '&units=metric' +\
     '&cnt=7' +\
     '&appid=' + str(self.get_owm_api_key())

  def get_request_output (self, url):
    opener = build_opener()
    request = Request(url)
    response = opener.open(request)
    return response

obj = Weather (45.41484, 4.398651)

"""
temperature :
  min - max   -> 
pluvio :
prévenir si c'est violent
"""
