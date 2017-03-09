

from __future__ import unicode_literals

from django.db import models

from hashlib import sha512
import os





class User (models.Model):

  """
    The User class maps the User table.
    It defines:
      - an ID ;
      - a login ;
      - a password ;
      - an email ;
      - a date of last login ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)

  EXPOSURE_NAMES = "", 
  EXPOSURES = enumerate (EXPOSURE_NAMES)
  exposure = models.PositiveSmallIntegerField (choices=EXPOSURES)

  # Definition of the relation-related attributes
  None

  @staticmethod
  def updating_session_operation (function):
    def updating_session_function (self, *args, **kwargs):
      self.updating_session_function ()
      return function (self, *args, **kwargs)
    return updating_session_function

  def update_last_operation (self):
    if self.session:
      self.session.update_last_operation ()

  def has_password (self, password):
    return str (sha512 (password + self.salt).digest ()) == self.password

  def is_connected (self):
    return self.session is not None and self.session.has_expired is False

  def disconnect (self):
    if self.session:
      self.session.delete ()

  def __hash__ (self):
    return str (sha512 (self.exposure).digest ()).encode ("base64")[:90]


class Exposure (models.Model):

  """
    The Exposure class maps the Exposure table.
    It defines:
      - an ID ;
      - an exposure ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)

  EXPOSURE_NAMES = "", 
  EXPOSURES = enumerate (EXPOSURE_NAMES)
  exposure = models.PositiveSmallIntegerField (choices=EXPOSURES)

  # Definition of the relation-related attributes
  None

  def __hash__ (self):
    return str (sha512 (self.exposure).digest ()).encode ("base64")[:90]


class LandscapeUse (models.Model):

  """
    The LandscapeUse class maps the LandscapeUse table.
    It defines:
      - an ID ;
      - a landscape ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)

  LANDSCAPE_NAMES = "", 
  LANDSCAPES = enumerate (LANDSCAPE_NAMES)
  landscape = models.PositiveSmallIntegerField (choices=LANDSCAPES)

  # Definition of the relation-related attributes
  None

  def __hash__ (self):
    return str (sha512 (self.landscape).digest ()).encode ("base64")[:90]


class Month (models.Model):

  """
    The Month class maps the month table.
    It defines:
      - an ID ;
      - a month ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)

  MONTH_NAMES = "January", "February", "March", "April", "May", "June", \
    "July", "August", "Septembre", "Octobre", "Novembre", "Decembre"
  MONTHS = enumerate (MONTH_NAMES)
  month = models.PositiveSmallIntegerField (choices=MONTHS)

  # Definition of the relation-related attributes
  None

  def __hash__ (self):
    return str (sha512 (self.month).digest ()).encode ("base64")[:90]


class Fruit (models.Model):

  """
    The Fruit class maps the fruit table.
    It defines:
      - an ID ;
      - a type ;
      - a colour ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)

  COLOUR_NAMES = "brown",
  COLOURS = enumerate (COLOUR_NAMES)
  colour = models.PositiveSmallIntegerField (choices=COLOURS)

  TYPE_NAMES = "capsule",
  TYPES = enumerate (TYPE_NAMES)
  type = models.PositiveSmallIntegerField (choices=TYPES)

  # Definition of the relation-related attributes
  months = models.ManyToManyField (Month)

  def __hash__ (self):
    return str (sha512 (self.colour + self.type).digest ()).encode ("base64")[:90]


class Flower (models.Model):

  """
    The Flower class maps the flower table.
    It defines:
      - an ID ;
      - a scent ;
      - a colour ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)

  COLOUR_NAMES = "brown",
  COLOURS = enumerate (COLOUR_NAMES)
  colour = models.PositiveSmallIntegerField (choices=COLOURS)

  SCENT_NAMES = "fragrant",
  SCENTS = enumerate (SCENT_NAMES)
  scent = models.PositiveSmallIntegerField (choices=SCENTS)

  # Definition of the relation-related attributes
  months = models.ManyToManyField (Month)

  def __hash__ (self):
    return str (sha512 (self.scent + self.colour).digest ()).encode ("base64")[:90]


class Plant (models.Model):

  """
    The Plant class maps the plant table.
    It defines:
      - an ID ;
      - a scientific name ;
      - a common name ;
      - a habit ;
      - a form ;
      - a height ;
      - a spread ;
      - a growth rate ;
      - a climate ;
      - the needed amount of water ;
      - the ability to flower ;
      - the ability to produce friuts ;
  """

  # Definition of the regular attributes.

  """
    To get the id of a plant, a SHA-512 algorithm is applied to the:
      common_name+scientific_name+salt
    The output length of a sha-512 is 64.
    The reason to use this kind of algorithm are:
      - ids are NOT indexes, so "1, 2, 3, ..." is not sementicaly correct ;
      - it prevents misspelling ids (for dangerous operation like deletion) ;
      - it prevent users to guess metadate like the number of entries we have ;
  """
  id = models.CharField (max_length=90, primary_key=True, unique=True)

  scientific_name = models.CharField (max_length=64, unique=True)
  common_name = models.CharField (max_length=64, unique=True)

  HABIT_NAMES = "twiggy",
  HABITS = enumerate (HABIT_NAMES)
  habit = models.PositiveSmallIntegerField (choices=HABITS)

  FORM_NAMES = "round",
  FORMS = enumerate (FORM_NAMES)
  form = models.PositiveSmallIntegerField (choices=FORMS)

  height = models.FloatField ()
  spread = models.FloatField ()

  GROWTH_RATE_NAMES = "moderate",
  GROWTH_RATES = enumerate (GROWTH_RATE_NAMES)
  growth_rate = models.PositiveSmallIntegerField (choices=GROWTH_RATES)

  CLIMATE_NAMES = "moderate",
  CLIMATES = enumerate (CLIMATE_NAMES)
  climate = models.PositiveSmallIntegerField (choices=CLIMATES)

  WATER_NAMES = "moderate",
  WATERS = enumerate (WATER_NAMES)
  water = models.PositiveSmallIntegerField (choices=WATERS)

  can_flower = models.BooleanField ()
  can_fruit = models.BooleanField ()

  # Definition of the relation-related attributes

  fruit = models.ForeignKey (Fruit, null=True)
  flower = models.ForeignKey (Flower, null=True)

  def __hash__ (self):
    return str (sha512 (self.common_name + self.scientific_name).digest ()).encode ("base64")[:90]

  def __str__(self):
    """
      A plant is identified by its common and sometimes its scientific name.
    """
    return "%s (%s)" % (self.common_name, self.scientific_name)


class Image (models.Model):

  """
    The Image class maps the image table.
    It defines:
      - an ID ;
      - a path to the cached image ;
      - a blob (the image) ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)
  blob = models.BinaryField (null=True)
  path = models.FilePathField ()

  # Definition of the relation-related attributes
  plants = models.ForeignKey (Plant, null=False)
  flowers = models.ForeignKey (Flower, null=False)
  fruits = models.ForeignKey (Fruit, null=False)

  def __hash__ (self):
    return str (sha512 (self.blob + self.path).digest ()).encode ("base64")[:90]
