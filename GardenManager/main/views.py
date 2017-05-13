

import os
import re
import json

from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.sessions.backends.db import SessionStore
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import Http404
from models import Plant, User, Ground, Project, Area, Position
from django.core.exceptions import ValidationError


def destroy_session_error (function):
  def destroyer (*args, **kwargs):
    returns = function (*args, **kwargs)
    for arg in args:
      if hasattr (arg, "session") and isinstance (arg.session, SessionStore):
        arg.session["error"] = ""
    return returns
  return destroyer


def need_logged_user (function):
  def destroyer (*args, **kwargs):
    for arg in args:
      if hasattr (arg, "session") and isinstance (arg.session, SessionStore):
        user = get_user (arg)
        if user.is_logged is False:
          raise Http404 ("Page not found.")
    return function (*args, **kwargs)
  return destroyer



def get_default_context (request, user=None, next_page=None, page_name=None):
  context = {
    "user": user or User (),
    "title": "The Garden Project",
    "error": request.session.get ("error", "There are not any error!!! lel"),
    "google_api_key": os.environ.get ("GOOGLE_MAPS_API_KEY", ""),
    "next_page": next_page or page_name or request.POST.get ("next_page", "/"),
    "js": [page_name] if page_name is not None else [], 
    "css": [page_name] if page_name is not None else [],
    "raw_resource": [], 
  }
  return context


def get_user (request):
  if request.session.get ("user_id", None) is None:
    return User ()
  return User.objects.get (id=request.session["user_id"])


@require_http_methods(["GET"])
@destroy_session_error
def root (request):
  user = get_user (request)
  context = get_default_context (request, user, next_page="/", page_name="root")
  context["flower_number"] = len (Plant.objects.all ())
  context["user_number"] = len (User.objects.all ())
  return render (request, "root.html", context=context)

@require_http_methods(["GET"])
@destroy_session_error
@need_logged_user
def home (request):
  user = get_user (request)
  context = get_default_context (request, user, page_name="home")
  context["projects"] = user.projects.all () or [
    type ('', (), {"name": "The following are test projects"}) (), 
    type ('', (), {"name": "Delete me"}) (), 
    type ('', (), {"name": "And me too"}) (), 
  ]
  context["delete_account_sentence"] = "Delete the account with login %s" % user.login
  return render (request, "home.html", context=context)

@require_http_methods(["GET"])
@destroy_session_error
@need_logged_user
def new_project (request):
  user = get_user (request)
  context = get_default_context (request, user, page_name="new", next_page="projects")
  context["js"] += ["google_map_api", "script_map"]
  context["css"].append ("creation_plan")
  context["raw_resource"].append (
    ("<script type=\"text/javascript\" async defer " + \
    "src=\"https://maps.googleapis.com/maps/api/js?" + \
    "key=%s&amp;libraries=drawing&amp;callback=initialize\"></script>") % \
    context["google_api_key"]
  )
  return render (request, "new.html", context=context)

@require_http_methods(["POST"])
@need_logged_user
def create_project (request):
  user = get_user (request)
  project = Project ()
  project.user = user
  project.name = request.POST.get ("new_project_name", None)
  area_points = json.loads(request.POST.get ("coordinate_set", "[]"))
  soil_type = Ground.GROUND_VALUES[Ground.GROUND_NAMES[-1]]
  for points in area_points:
    other_points = points[1:]
    area = Area ()
    area.x, area.y = points[0]
    area.ground = Ground.objects.filter (ground=int (soil_type))[0]
    positions = [Position (**kwargs) for kwargs in 
      [dict ((('x', point[0]), ('y', point[1]))) for point in points[1:]]]
    for position in positions:
      position.save ()
    area.positions = positions
    area.save ()
  try:
    project.save ()
    user.projects.add (project)
    user.save ()
  except ValidationError:
    request.session["error"] = "You already have a project with this name."
    return HttpResponseRedirect ("new")
  return HttpResponseRedirect ("projects")

@require_http_methods(["GET"])
@destroy_session_error
@need_logged_user
def view_projects (request):
  user = get_user (request)
  context = get_default_context (request, user, page_name="projects")
  context["projects"] = user.projects.all ()
  return render (request, "projects.html", context=context)

@require_http_methods(["GET"])
@destroy_session_error
def info (request):
  user = get_user (request)
  context = get_default_context (request, user, page_name="info")
  return render (request, "info.html", context=context)

@require_http_methods(["POST"])
@need_logged_user
def remove_user (request):
  user = get_user (request)
  context = get_default_context (request, user, page_name="info")
  if request.POST["magic_sentence"] == "Delete the account with login %s" % user.login:
    user.delete ()
    del request.session["user_id"]
    request.session["error"] = "Your account has been deleted successfully"
    return HttpResponseRedirect ("/")
  else:
    request.session["error"] = "Wrong magic sentence"
    return HttpResponseRedirect ("/home")


@require_http_methods(["POST"])
def login (request):
  user = get_user (request)
  if not user.is_logged:
    login = request.POST.get ("login", "")
    password = request.POST.get ("password", "")
    try:
      logged_user = User.objects.get (login=login)
    except ObjectDoesNotExist:
      logged_user = None
    if logged_user is None:
      request.session["error"] = "Unknown login: '%s'" % login
    elif logged_user.has_password (password):
      user = logged_user
      request.session["user_id"] = user.id
      request.session["error"] = "Connexion success"
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
  elif re.match ("(^[a-zA-Z0-9_.+\-!#$%&'*/=?^`{|}~;]{1,64}@[a-zA-Z0-9-]" \
      "{1,251}\.[a-zA-Z0-9-.]+$)", mail) is None:
    request.session["error"] = "Bad email adress."
  else:
    user = User ()
    user.login = unicode (login)
    user.password = unicode (password)
    user.email = unicode (mail)
    user.save ()
    request.session["user_id"] = user.id
  request.session["_old_post"] = request.POST
  if redirect_page is not None:
    return HttpResponseRedirect (redirect_page)
  return HttpResponseRedirect ("/")


@require_http_methods(["GET"])
def logout (request):
  if request.session.has_key ("user_id"):
    request.session["error"] = "Logout success"
    del request.session["user_id"]
  else:
    request.session["error"] = "You are not logged"
  redirect_page = request.GET.get ("next_page", None)
  request.session["_old_post"] = request.POST
  return HttpResponseRedirect ("/")
