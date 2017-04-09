

import os
import re

from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from models import User



def get_default_context (request, user=None, next_page=None):
  context = {
    "user": user or User (),
    "title": "Garden Project",
    "error": request.session.get ("error", "There are not any error!!! lel"),
    "google_api_key": os.environ.get ("GOOGLE_MAPS_API_KEY", ""),
    "next_page": next_page or request.POST.get ("next_page", "/"),
  }
  return context


def get_user (request):
  if request.session.get ("user_id", None) is None:
    return User ()
  return User.objects.get (id=request.session["user_id"])


@require_http_methods(["GET"])
def root (request):
  user = get_user (request)
  context = get_default_context (request, user)
  return render (request, "root.html", context=context)


@require_http_methods(["GET"])
def home (request):
  user = get_user (request)
  context = get_default_context (request, user)
  return render (request, "home.html", context=context)


@require_http_methods(["POST"])
def login (request):
  request.session["error"] = ""
  user = get_user (request)
  if not user.is_logged:
    login = request.POST.get ("login", "")
    password = request.POST.get ("user_password", "")
    try:
      logged_user = User.objects.get (login=login)
    except ObjectDoesNotExist:
      logged_user = None
    if logged_user is None:
      request.session["error"] = "Unknown login: '%s'" % login
    elif logged_user.has_password (password):
      user = logged_user
      request.session["user_id"] = user.id
    else:
      request.session["error"] = "Bad password"
  else:
    request.session["error"] = "You are already logged as '%s'" % user.login
  redirect_page = request.GET.get ("next_page", None)
  request.session["_old_post"] = request.POST
  if redirect_page is not None:
    return HttpResponseRedirect (redirect_page)
  return HttpResponseRedirect ("/")


@require_http_methods(["POST"])
def register (request):
  request.session["error"] = ""
  redirect_page = request.GET.get ("next_page", None)
  login = request.POST.get ("register_user_login", None)
  password = request.POST.get ("register_user_password", None)
  password_verif = request.POST.get ("register_user_password_verif", None)
  mail = request.POST.get ("register_user_mail", None)
  missing_fields = set ([name for value, name in zip (
    (login, password, password_verif, mail),
    ("login", "password", "password (verif.)", "mail")) if value is None])
  if not all ([login, password, password_verif, mail]):
    request.session["error"] = \
      "Missing field in register form: %s" % repr (missing_fields)
  elif password != password_verif:
    request.session["error"] = "Password does not match"
  elif len (password) < 6 or len (password) > 256:
    request.session["error"] = "Password must be between 6 and 256 chars long."
  elif re.match ("(^[a-zA-Z0-9_.+\-!#$%&'*/=?^`{|}~;]{1,64}@[a-zA-Z0-9-]{1,251}\.[a-zA-Z0-9-.]+$)", mail) is None:
    request.session["error"] = "Bad email adress."
  else:
    user = User ()
    user.login = unicode (login)
    user.password = unicode (password)
    user.email = unicode (mail)
    user.save ()
    copy = User.objects.get (id=user.id)
    print user.id, user.login, user.password, user.email, user.salt, user.last_login
    print copy.id, copy.login, copy.password, copy.email, copy.salt, copy.last_login
    #request.session["user_id"] = user.id
  request.session["_old_post"] = request.POST
  if redirect_page is not None:
    return HttpResponseRedirect (redirect_page)
  return HttpResponseRedirect ("/")


@require_http_methods(["GET"])
def logout (request):
  request.session["error"] = ""
  del request.session["user_id"]
  redirect_page = request.GET.get ("next_page", None)
  request.session["_old_post"] = request.POST
  if redirect_page is not None:
    return HttpResponseRedirect (redirect_page)
  return HttpResponseRedirect ("/")
