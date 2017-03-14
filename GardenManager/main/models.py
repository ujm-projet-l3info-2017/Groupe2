

from __future__ import unicode_literals
import time

from django.db import models

from digester import Digester


def set_class_attribute (attributes):
  print attributes
  def attr_setter (cls):
    for attribute, value in attributes.iteritems ():
      setattr (cls, attribute, value)
    return cls
  return attr_setter


class Ground (models.Model):

  """
    The Ground class maps the Ground table.
    It defines:
      - an id ;
      - a name ;
      - a type ;
      - a pH ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)
  name = models.CharField (max_length=32)
  ph = models.FloatField (null=False)

  TYPE_NAMES = "", 
  TYPES = enumerate (TYPE_NAMES)
  type = models.PositiveSmallIntegerField (choices=TYPES)

  # Definition of the relation-related attributes
  None

  def digest (self):
    return Digester ().digest (self.name + str (self.ph) + str (self.type))


class Session (models.Model):

  """
    The Session class maps the Session table.
    It defines:
      - a user_id ;
      - a last_operation ;
      - a cookie ;
  """

  # Definition of the regular attributes.

  user_id = models.CharField (max_length=90, primary_key=True, unique=True)
  last_operation = models.DateField (auto_now=True)
  cookie = models.CharField (max_length=256)

  # Definition of the relation-related attributes
  None

  def update_last_operation (self):
    # with auto_now, the last_operation field will be updated at each save op.
    self.save ()

  def digest (self):
    return Digester ().digest (self.user_id)


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
  session = models.ForeignKey (Session, null=True)

  @staticmethod
  def updating_session_operation (function):
    def updating_session_function (self, *args, **kwargs):
      self.update_last_operation ()
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

  def digest (self):
    return Digester ().digest (self.exposure)


class Project (models.Model):

  """
    The Session class maps the Session table.
    It defines:
      - an id ;
      - a name ;
      - a creation date ;
      - an update date ;
  """

  def validate_name (name):
    if self.user.projects.filter (name=name) is not None:
      raise ValidationError('Already existing project with name: %s' % name,
        code='invalid')

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)
  name = models.CharField (max_length=32)
  creation_date = models.DateField ()
  update_date = models.DateField (auto_now=True)

  # Definition of the relation-related attributes
  user = models.ForeignKey (User, null=True)

  def save (self):
    """
      This save check for the existance of another project with the same name.
      If one is found, throw a ValidationError.
    """
    super (Project, self).save ()

  def digest (self):
    return Digester (salt=True).digest ()


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

  def digest (self):
    return Digester ().digest (self.exposure)


class LandscapeUse (models.Model):

  """
    The LandscapeUse class maps the LandscapeUse table.
    It defines:
      - an ID ;
      - a landscape ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)

  LANDSCAPE_NAMES = "All", "Accent plant", "Alpine", "Aquatic - ponds",        \
    "Attract beneficial insects", "Attract birds", "Attract butterflies",      \
    "Bedding plant", "Container planting", "Cut flower or foliage",            \
    "Dried flower or fruit", "Dryland", "Erosion control",       \
    "Espalier", "Fall interest", "Filler", "Floristry", "Forestry",            \
    "Fragrance", "Golf green", "Green roof technology", "Green walls",         \
    "Ground cover", "Group or mass planting", "Hanging basket", "Hedge row",   \
    "Herb", "Indoor plant", "Lawn - sports field", "Medicinal plant",          \
    "Mixed shrub border", "Native planting", "Perennial border", "Reclamation",\
    "Rock garden", "Screening", "Security/barrier", "Shade tree",              \
    "Sheared hedge", "Small garden/space", "Specimen plant", "Spring interest",\
    "Street", "Summer interest", "Tall background", "Topiary",\
    "Urban agriculture", "Waterside planting", "Wetland - bogs",               \
    "Wild flower garden", "Wildlife food", "Wind break", "Winter interest",    \
    "Woodland margin"
  LANDSCAPES = enumerate (LANDSCAPE_NAMES)
  LANDSCAPE_VALUES = dict (map (lambda x:x[::-1], LANDSCAPES))
  landscape = models.PositiveSmallIntegerField (choices=LANDSCAPES)

  # Definition of the relation-related attributes
  None

  def digest (self):
    return Digester ().digest (self.landscape)


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

  def digest (self):
    return Digester ().digest (self.month)


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
    return Digester ().digest (self.colour + self.type)


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

  def digest (self):
    return Digester ().digest (self.scent + self.colour)

#@set_class_attribute(dict (map (lambda _:_[::-1],
  #enumerate (map ("ZONE_{}".format, range (1, 12)+["8A", "8B"])))))
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

  HABIT_NAMES = "all", "arching", "dense", "epiphytic", "fastigiate", \
    "horizontal", "irregular", "open", "pendulous", "spreading", \
    "stiffly upright", "twiggy", "upright"
  HABITS = enumerate (HABIT_NAMES)
  HABIT_VALUE = dict (map (lambda _:_[::-1], HABITS))
  habit = models.PositiveSmallIntegerField (choices=HABITS)

  FORM_NAMES = "all", "climbing", "columnar", "creeping / mat-like",        \
    "irregular", "mounded", "oval - horizontal", "oval - vertical",         \
    "pyramidal - narrowly", "pyramidal - widely", "round", "vase", "weeping"
  FORMS = enumerate (FORM_NAMES)
  FORM_VALUE = dict (map (lambda _:_[::-1], FORMS))
  form = models.PositiveSmallIntegerField (choices=FORMS)

  spread_min = models.FloatField (null=True)
  spread_max = models.FloatField (null=True)
  height_min = models.FloatField (null=True)
  height_max = models.FloatField (null=True)

  GROWTH_RATE_NAMES = "fast", "moderate", "slow"
  GROWTH_RATES = enumerate (GROWTH_RATE_NAMES)
  GROWTH_RATE_VALUE = dict (map (lambda _:_[::-1], GROWTH_RATES))
  growth_rate = models.PositiveSmallIntegerField (choices=GROWTH_RATES)

  CLIMATE_NAMES = map ("ZONE_{}".format, range (1, 12)+["8A", "8B"])
  CLIMATES = enumerate (CLIMATE_NAMES)
  CLIMATE_VALUE = dict (map (lambda _:_[::-1], CLIMATES))
  DEFAULT_CLIMATE = 5
  climate = models.PositiveSmallIntegerField (choices=CLIMATES)

  WATER_NAMES = "low", "moderate", "unknown", "high"
  WATERS = enumerate (WATER_NAMES)
  WATER_VALUE = dict (map (lambda _:_[::-1], WATERS))
  water = models.PositiveSmallIntegerField (choices=WATERS)

  can_flower = models.BooleanField (default=False)
  can_fruit = models.BooleanField (default=False)

  # Definition of the relation-related attributes

  fruit = models.ForeignKey (Fruit, null=True, related_name="plants")
  flower = models.ForeignKey (Flower, null=True, related_name="plants")
  landscapes = models.ManyToManyField (LandscapeUse, null=True,
    related_name="plants")

  def __init__ (self, *args, **kwargs):
    super (Plant, self).__init__ (*args, **kwargs)
    self.id = self.digest ()

  def digest (self):
    return Digester ().digest (self.common_name + self.scientific_name)

  def __str__(self):
    return repr (self)

  def __repr__ (self):
    return ('\n'.join (("Plant object of id %(id)s ({ ", 
      "\tscientific name  = %(scientific_name)s", 
      "\tcommon name      = %(common_name)s", 
      "\thabit            = %(habit)s", 
      "\tform             = %(form)s", 
      "\theight           = %(height_min)s - %(height_max)s", 
      "\tspread           = %(spread_min)s - %(spread_max)s", 
      "\tgrowth rate      = %(growth_rate)s", 
      "\tclimate          = %(climate)s", 
      "\twater            = %(water)s", 
      "\tcan flower       = %(can_flower)s", 
      "\tcan fruit        = %(can_fruit)s", 
      "})"
    )) % {
      "scientific_name" : self.scientific_name,
      "common_name" : self.common_name,
      "habit" : self.habit if self.habit else "unknown",
      "form" : self.form if self.form else "unknown",
      "height_min" : self.height_min if self.height_min else "unknown",
      "height_max" : self.height_max if self.height_max else "unknown",
      "spread_min" : self.spread_min if self.spread_min else "unknown",
      "spread_max" : self.spread_max if self.spread_max else "unknown",
      "growth_rate" : self.growth_rate if self.growth_rate else "unknown",
      "climate" : self.climate if self.climate else "unknown",
      "water" : self.water if self.water else "unknown",
      "can_flower" : "?" if self.can_flower is None else self.can_flower,
      "can_fruit" : "?" if self.can_fruit is None else self.can_fruit,
      "id": self.id,
    })


class Area (models.Model):

  """
    The Area class maps the Area table.
    It defines:
      - an id ;
      - a x position ;
      - a y position ;
      - a ground_id ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)
  x = models.FloatField (null=False)
  y = models.FloatField (null=False)

  # Definition of the relation-related attributes
  ground = models.ForeignKey (Ground, null=False, related_name="areas")

  def digest (self):
    return Digester ().digest (str (self.x) + str (self.y) + self.ground_id)


class PlantSpot (models.Model):

  """
    The PlantSpot class maps the PlantSpot table.
    It defines:
      - an id ;
      - a position id ;
      - a plant id ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)

  # Definition of the relation-related attributes
  plant = models.ForeignKey (Plant, null=False, related_name="plant_spots")
  area = models.ForeignKey (Area, null=False, related_name="plant_spots")

  def digest (self):
    # juste a random salt hashed
    return Digester (salt=True, salt_length=64, cutoff=90).digest ()


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
  plant = models.ForeignKey (Plant, null=True, related_name="images")
  flower = models.ForeignKey (Flower, null=True, related_name="images")
  fruit = models.ForeignKey (Fruit, null=True, related_name="images")

  def digest (self):
    return Digester ().digest (self.blob + self.path)


class Position (models.Model):

  """
    The Position class maps the Position table.
    It defines:
      - an id ;
      - an x ;
      - an y ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)
  x = models.FloatField ()
  y = models.FloatField ()

  # Definition of the relation-related attributes
  area = models.ForeignKey (Area, null=True, related_name="positions")
  plant_spot = models.ForeignKey (PlantSpot, null=True, related_name="positions")

  def digest (self):
    # juste a random salt hashed
    return Digester ().digest (str (self.x) + ';' + str (self.y))
