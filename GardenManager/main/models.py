

from __future__ import unicode_literals
import time

from django.db import models

from utils.digester import Digester
from utils.circular_list import CircularList


def set_class_attribute (attributes):
  print attributes
  def attr_setter (cls):
    for attribute, value in attributes.iteritems ():
      setattr (cls, attribute, value)
    return cls
  return attr_setter


class Colour (models.Model):

  """
    The Colour class maps the Colour table.
    It defines:
      - an id ;
      - a colour ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)

  COLOUR_NAMES = "all", "white", "orange", "yellow", "green-yellow", "green",  \
    "blue", "violet", "purple", "pink", "magenta", "red", "dark-red", "brown", \
    "bronze", "silver", "black", "unknown"
  COLOURS = tuple (enumerate (COLOUR_NAMES))
  COLOUR_VALUES = dict (map (lambda x:x[::-1], COLOURS))
  colour = models.PositiveSmallIntegerField (choices=COLOURS, null=True)

  # Definition of the relation-related attributes
  None

  def __init__ (self, *args, **kwargs):
    super (Colour, self).__init__ (*args, **kwargs)
    self.id = self.digest ()

  def digest (self):
    return Digester ().digest (str (self))

  def str_colour (self):
    return Colour.COLOUR_NAMES[self.colour]

  def __str__ (self):
    return "Colour (%s)" % self.str_colour ()

  def __repr__ (self):
    return ('\n'.join (("Colour object of id %(id)s ({ ",
      "\tcolour            = %(colour)s",
      "})")) % { "id": self.id, "colour": self.str_colour () })


class Ground (models.Model):

  """
    The Ground class maps the Ground table.
    It defines:
      - an id ;
      - a ground ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)

  GROUND_NAMES = "all", "acidic", "bog", "well-drained", "humus rich", \
    "alkaline", "rocky or gravelly or dry", "unknown", 
  GROUNDS = tuple (enumerate (GROUND_NAMES))
  GROUND_VALUES = dict (map (lambda x:x[::-1], GROUNDS))
  ground = models.PositiveSmallIntegerField (choices=GROUNDS, null=True)

  #ph = models.FloatField (null=True)
  PH_VALUES = {
    "all":2, "neutral": 2, "acidic":1, "bog": 1, "well-drained": 1, \
    "humus rich": 1, "rocky or gravelly or dry": 3, "alkaline": 3,
    "unknown": 2
  }
  PH_EQUIVALANCES = {
    lambda x:x < 7: PH_VALUES["acidic"],
    lambda x:x > 7: PH_VALUES["alkaline"],
    lambda x:x == 7: PH_VALUES["neutral"],
  }

  # Definition of the relation-related attributes
  None

  def __init__ (self, *args, **kwargs):
    super (Ground, self).__init__ (*args, **kwargs)
    """
    if kwargs.has_key ("ph") is False and self.ground is not None:
      self.ph = Ground.PH_VALUES[Ground.GROUND_NAMES[self.ground]]
    """
    self.id = self.digest ()

  def digest (self):
    return Digester ().digest (str (self))

  def __str__ (self):
    return "Ground (%s)" % Ground.GROUND_NAMES[self.ground]

  def __repr__ (self):
    return ('\n'.join (("Ground object of id %(id)s ({ ",
      "\ttype             = %(ground)s",
      "\tph               = %(ph)s",
      "})")) % { "id": self.id, "ground": Ground.GROUND_NAMES[self.ground], "ph": self.ph })


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

  login = models.CharField (max_length=32, null=True)
  password = models.CharField (max_length=90, null=True)
  email = models.EmailField (null=True)
  last_login = models.DateField (auto_now=True)

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

  EXPOSURE_NAMES = "moderate", "filtered shade", "full sun", \
    "part sun/part shade", "full sun only if soil kept moist", \
    "deep shade", "sheltered", "unknown"
  EXPOSURES = tuple (enumerate (EXPOSURE_NAMES))
  EXPOSURE_VALUES = dict (map (lambda x:x[::-1], EXPOSURES))
  exposure = models.PositiveSmallIntegerField (choices=EXPOSURES)

  # Definition of the relation-related attributes
  None

  def __init__ (self, *args, **kwargs):
    super (Exposure, self).__init__ (*args, **kwargs)
    self.id = self.digest ()

  def digest (self):
    return Digester ().digest (str (self))

  def __str__ (self):
    return "Exposure (%s)" % Exposure.EXPOSURE_NAMES[self.exposure]

  def __repr__ (self):
    return ('\n'.join (("Exposure object of id %(id)s ({ ",
      "\texposure  = %(exposure)s",
      "})")) % { "id": self.id, "exposure": str (self)
    })


class LandscapeUse (models.Model):

  """
    The LandscapeUse class maps the LandscapeUse table.
    It defines:
      - an ID ;
      - a landscape ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)

  UNSPECIFIED_LANDSCAPE_NAMES = "Arbors or trellis", 
  LANDSCAPE_NAMES = "All", "Accent plant", "Alpine", "Aquatic - ponds",        \
    "Attract beneficial insects", "Attract birds", "Attract butterflies",      \
    "Bedding plant", "Container planting", "Cut flower or foliage",            \
    "Dried flower or fruit", "Dryland", "Erosion control",                     \
    "Espalier", "Fall interest", "Filler", "Floristry", "Forestry",            \
    "Fragrance", "Golf green", "Green roof technology", "Green walls",         \
    "Ground cover", "Group or mass planting", "Hanging basket", "Hedge row",   \
    "Herb", "Indoor plant", "Lawn - sports field", "Medicinal plant",          \
    "Mixed shrub border", "Native planting", "Perennial border", "Reclamation",\
    "Rock garden", "Screening", "Security/barrier", "Shade tree",              \
    "Sheared hedge", "Small garden/space", "Specimen plant", "Spring interest",\
    "Street", "Summer interest", "Tall background", "Topiary",                 \
    "Urban agriculture", "Waterside planting", "Wetland - bogs",               \
    "Wild flower garden", "Wildlife food", "Wind break", "Winter interest",    \
    "Woodland margin", "unknown"
  LANDSCAPE_NAMES += UNSPECIFIED_LANDSCAPE_NAMES
  LANDSCAPES = tuple (enumerate (LANDSCAPE_NAMES))
  LANDSCAPE_VALUES = dict (map (lambda x:x[::-1], LANDSCAPES))
  landscape = models.PositiveSmallIntegerField (choices=LANDSCAPES)

  # Definition of the relation-related attributes
  None

  def __init__ (self, *args, **kwargs):
    super (LandscapeUse, self).__init__ (*args, **kwargs)
    self.id = self.digest ()

  def set_landscape (self, name):
    if LandscapeUse.LANDSCAPE_VALUES.has_key (name):
      self.landscape = LandscapeUse.LANDSCAPE_VALUES[name]

  def digest (self):
    return Digester ().digest (str (self))

  def str_landscape (self):
    return LandscapeUse.LANDSCAPE_NAMES[self.landscape]

  def __str__ (self):
    return "Landscape (%s)" % self.str_landscape ()

  def __repr__ (self):
    return ('\n'.join (("Landscape object of id %(id)s ({ ",
      "\tlandscape use    = %(landscape)s",
      "})")) % { "id": self.id, "landscape": str (self)
    })


class Month (models.Model):

  """
    The Month class maps the month table.
    It defines:
      - an ID ;
      - a month ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)

  MONTH_NAMES = CircularList (("january", "february", "march", "april", "may", \
    "june", "july", "august", "septembre", "octobre", "novembre", "decembre"))
  MONTHS = tuple (enumerate (MONTH_NAMES))
  MONTH_VALUES = dict (map (lambda _:_[::-1], MONTHS))
  MONTH_FULL_NAME = { month[:3]: month for month in MONTH_NAMES }
  month = models.PositiveSmallIntegerField (choices=MONTHS)

  # Definition of the relation-related attributes
  None

  def __init__ (self, *args, **kwargs):
    super (Month, self).__init__ (*args, **kwargs)
    self.id = self.digest ()

  def from_to (self, start, stop, step=1):
    start_index, stop_index = map (Month.MONTH_NAMES.index, (start, stop))
    return Month.MONTH_NAMES[start_index:stop_index:step]

  def digest (self):
    return Digester ().digest (str (self))

  def str_month (self):
    return list (Month.MONTH_NAMES[self.month])[0]

  def __str__ (self):
    return "Month (%s)" % self.str_month ()

  def __repr__ (self):
    return ('\n'.join (("Month object of id %(id)s ({ ",
      "\tmonth            = %(month)s",
      "})")) % { "id": self.id, "month": str (self)
    })


class FruitType (models.Model):

  """
    The FruitType class maps the fruit_type table.
    It defines:
      - an ID ;
      - a type ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)
  # id is auto-inc 'cause two flowers can be similare without being the same.

  TYPE_NAMES = "All", "Aggregate fruit", "Achene", "Berry", "Capsule",         \
    "Cypsela", "Drupe", "Edible", "Follicle", "Grain", "Hesperidium", "Legume",\
    "Multiple fruit", "Nut", "Pepo", "Pome", "Samara", "Schizocarp", "Silicle",\ 
    "Silique", "Aborted or absent", "Cone", "Sporangium", "unknown"

  TYPES = tuple (enumerate (TYPE_NAMES))
  TYPE_VALUES = dict (map (lambda _:_[::-1], TYPES))
  type = models.PositiveSmallIntegerField (choices=TYPES)

  # Definition of the relation-related attributes
  None

  def __init__ (self, *args, **kwargs):
    super (FruitType, self).__init__ (*args, **kwargs)
    self.id = self.digest ()

  def digest (self):
    return Digester ().digest (str (self))

  def str_type (self):
    return FruitType.TYPE_NAMES[self.type]

  def __str__ (self):
    return "FruitType (%s)" % self.str_type ()

  def __repr__ (self):
    return ('\n'.join (("FruitType object of id %(id)s ({ ",
      "\ttype             = %(type)s",
      "})")) % { "id": str (self.id), "type": self.str_type () })


class Fruit (models.Model):

  """
    The Fruit class maps the fruit table.
    It defines:
      - an ID ;
      - some type ;
      - some colours ;
      - some fruit time.
  """

  # Definition of the regular attributes.
  id = models.CharField (max_length=90, primary_key=True, unique=True)

  # Definition of the relation-related attributes
  colours = models.ManyToManyField (Colour, related_name="fruits")
  types = models.ManyToManyField (FruitType, related_name="fruits")
  months = models.ManyToManyField (Month, related_name="fruits")
  None

  def __init__ (self, *args, **kwargs):
    super (Fruit, self).__init__ (*args, **kwargs)
    self.update_id ()

  def update_id (self):
    self.id = self.digest ()

  def digest (self):
    return Digester (salt=True).digest ('')# str (self))

  def str_colour (self):
    return ', '.join ([colour.str_colour () for colour in self.colours.all ()])

  def str_month (self):
    return ', '.join ([month.str_month () for month in self.months.all ()])

  def str_type (self):
    return ', '.join ([fruit_type.str_type () \
      for fruit_type in self.types.all ()])

  def __str__ (self):
    return "Fruit (colours are %s ; types are %s ; fruiting times are %s)" % (
      self.str_colour (), self.str_type (), self.str_month ())

  def __repr__ (self):
    return ('\n'.join (("Fruit object of id %(id)s ({ ",
      "\tcolour           = %(colour)s",
      "})")) % { "id": str (self.id), "colour": self.str_colour () })


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

  colours = models.ManyToManyField (Colour, related_name="flowers")

  SCENT_NAMES = "fragrant", 
  SCENTS = tuple (enumerate (SCENT_NAMES))
  scent = models.PositiveSmallIntegerField (choices=SCENTS)

  # Definition of the relation-related attributes
  months = models.ManyToManyField (Month)
  None

  def __init__ (self, *args, **kwargs):
    super (Flower, self).__init__ (*args, **kwargs)
    self.update_id ()

  def update_id (self):
    self.id = self.digest ()

  def digest (self):
    return Digester (salt=True).digest ('')# str (self))

  def str_colour (self):
    return ', '.join (colour.str_colour () for colour in self.colours.all ())

  def str_scent (self):
    return Flower.SCENT_NAMES[self.scent]

  def __str__ (self):
    return "Flower (colour is %s ; scent is %s)" % (self.str_colour (), self.str_scent ())

  def __repr__ (self):
    return ('\n'.join (("Flower object of id %(id)s ({ ",
      "\tcolours          = %(colours)s",
      "})")) % { "id": self.id, "colours": self.str_colour ()
    })


class Habit (models.Model):

  """
    The Habit class maps the habit table.
    It defines:
      - an ID ;
      - a habit name ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)

  HABIT_NAMES = "all", "arching", "dense", "epiphytic", "fastigiate", \
    "horizontal", "irregular", "open", "pendulous", "spreading", \
    "stiffly upright", "twiggy", "upright", "unknown"
  HABITS = tuple (enumerate (HABIT_NAMES))
  HABIT_VALUES = dict (map (lambda _:_[::-1], HABITS))
  habit = models.PositiveSmallIntegerField (choices=HABITS)

  # Definition of the relation-related attributes
  None

  def __init__ (self, *args, **kwargs):
    super (Habit, self).__init__ (*args, **kwargs)
    self.id = self.digest ()

  def digest (self):
    return Digester ().digest (str (self))

  def str_habit (self):
    return Habit.HABIT_NAMES[self.habit]

  def __str__ (self):
    return "Habit (%s)" % self.str_habit ()

  def __repr__ (self):
    return ('\n'.join (("Habit object of id %(id)s ({ ",
      "\thabit            = %(habit)s",
      "})")) % { "id": self.id, "habit": str (self)
    })


class Form (models.Model):

  """
    The Form class maps the form table.
    It defines:
      - an ID ;
      - a form name ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)

  FORM_NAMES = "all", "climbing", "columnar", "creeping / mat-like",          \
    "irregular", "mounded", "oval - horizontal", "oval - vertical",           \
    "pyramidal - narrowly", "pyramidal - widely", "round", "vase", "weeping", \
    "unknown"
  FORMS = tuple (enumerate (FORM_NAMES))
  FORM_VALUES = dict (map (lambda _:_[::-1], FORMS))
  form = models.PositiveSmallIntegerField (choices=FORMS)

  # Definition of the relation-related attributes
  None

  def __init__ (self, *args, **kwargs):
    super (Form, self).__init__ (*args, **kwargs)
    self.id = self.digest ()

  def digest (self):
    return Digester ().digest (str (self))

  def str_form (self):
    return Form.FORM_NAMES[self.form]

  def __str__ (self):
    return "Form (%s)" % self.str_form ()

  def __repr__ (self):
    return ('\n'.join (("Form object of id %(id)s ({ ",
      "\tform             = %(form)s",
      "})")) % { "id": self.id, "form": str (self)
    })


class Water (models.Model):

  """
    The Water class maps the water table.
    It defines:
      - an ID ;
      - a Water frequency ;
  """

  # Definition of the regular attributes.

  id = models.CharField (max_length=90, primary_key=True, unique=True)

  WATER_NAMES = "low", "moderate", "high", "wetlands", "summer dry", \
    "aquatic", "winter dry", "dryland", "unknown"
  WATERS = tuple (enumerate (WATER_NAMES))
  WATER_VALUES = dict (map (lambda _:_[::-1], WATERS))
  water = models.PositiveSmallIntegerField (choices=WATERS)

  # Definition of the relation-related attributes
  None

  def __init__ (self, *args, **kwargs):
    super (Water, self).__init__ (*args, **kwargs)
    self.id = self.digest ()

  def digest (self):
    return Digester ().digest (str (self))

  def str_water (self):
    return Water.WATERS[self.water][1]

  def __str__ (self):
    return "Water (%s)" % self.str_water ()

  def __repr__ (self):
    return ('\n'.join (("Water object of id %(id)s ({ ",
      "\twater frequency  = %(water)s",
      "})")) % { "id": self.id, "water": str (self)
    })


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

  scientific_name = models.CharField (max_length=64)
  common_name = models.CharField (max_length=64)

  spread_min = models.FloatField (null=True)
  spread_max = models.FloatField (null=True)
  height_min = models.FloatField (null=True)
  height_max = models.FloatField (null=True)

  GROWTH_RATE_NAMES = "fast", "moderate", "slow", "unknown"
  GROWTH_RATES = enumerate (GROWTH_RATE_NAMES)
  GROWTH_RATE_VALUE = dict (map (lambda _:_[::-1], GROWTH_RATES))
  growth_rate = models.PositiveSmallIntegerField (choices=GROWTH_RATES)

  CLIMATE_NAMES = map ("ZONE_{}".format, range (1, 12)+["8A", "8B"]) + ["unknown"]
  CLIMATES = enumerate (CLIMATE_NAMES)
  CLIMATE_VALUE = dict (map (lambda _:_[::-1], CLIMATES))
  DEFAULT_CLIMATE = 5
  DEFAULT_CLIMATE_NAME = CLIMATE_NAMES[DEFAULT_CLIMATE]
  climate = models.PositiveSmallIntegerField (choices=CLIMATES)

  can_flower = models.BooleanField (default=False)
  can_fruit = models.BooleanField (default=False)

  # Definition of the relation-related attributes

  fruit = models.ForeignKey (Fruit, null=True, related_name="plants")
  flower = models.ForeignKey (Flower, null=True, related_name="plants")
  landscapes = models.ManyToManyField (LandscapeUse, related_name="plants")
  exposures = models.ManyToManyField (Exposure, related_name="plants")
  habits = models.ManyToManyField (Habit, related_name="plants")
  forms = models.ManyToManyField (Form, related_name="plants")
  waters = models.ManyToManyField (Water, related_name="plants")
  grounds = models.ManyToManyField (Ground, related_name="plants")
  plantation_time = models.ManyToManyField (Month, related_name="plants")

  def __init__ (self, *args, **kwargs):
    super (Plant, self).__init__ (*args, **kwargs)
    self.id = self.digest ()

  def digest (self):
    return Digester ().digest (self.common_name + self.scientific_name)

  def str_growth_rate (self):
    return Plant.GROWTH_RATE_NAMES[self.growth_rate or -1].lower ().capitalize ()

  def str_climate (self):
    return Plant.CLIMATE_NAMES[self.climate or -1].lower ().capitalize ()

  def __str__(self):
    return "Plant (%s ; %s)" % (self.common_name, self.scientific_name)

  def __repr__ (self):
    return ('\n'.join (("Plant object of id %(id)s ({ ", 
      "\tscientific name  = %(scientific_name)s", 
      "\tcommon name      = %(common_name)s", 
      "\thabit            = %(habits)s", 
      "\texposure         = %(exposure)s", 
      "\tground           = %(ground)s", 
      "\tform             = %(form)s", 
      "\tflower           = %(flower)s", 
      "\tfruit            = %(fruit)s", 
      "\theight           = %(height_min)s - %(height_max)s", 
      "\tspread           = %(spread_min)s - %(spread_max)s", 
      "\tgrowth rate      = %(growth_rate)s", 
      "\tclimate          = %(climate)s", 
      "\tplantation time  = %(plantation_time)s", 
      "\twater            = %(water)s", 
      "\tlandscape        = %(landscape)s", 
      "\tcan flower       = %(can_flower)s", 
      "\tcan fruit        = %(can_fruit)s", 
      "})"
    )) % {
      "scientific_name" : self.scientific_name,
      "common_name" : self.common_name,
      "habits" : map (str, self.habits.all ()) if self.habits else "unknown",
      "exposure" : map (str, self.exposures.all ()) if self.exposures else "unknown",
      "ground" : map (str, self.grounds.all ()) if self.grounds else "unknown",
      "form" : map (str, self.forms.all ()) if self.forms else "unknown",
      "flower" : str (self.flower) if self.flower else "unknown",
      "fruit" : str (self.fruit) if self.fruit else "unknown",
      "height_min" : self.height_min if self.height_min else "unknown",
      "height_max" : self.height_max if self.height_max else "unknown",
      "spread_min" : self.spread_min if self.spread_min else "unknown",
      "spread_max" : self.spread_max if self.spread_max else "unknown",
      "growth_rate" : self.str_growth_rate () if self.growth_rate is not None else "unknown",
      "climate" : self.str_climate () if self.climate is not None else "unknown",
      "plantation_time" : map (str, self.plantation_time.all ()),
      "water" : map (str, self.waters.all ()) if self.waters else "unknown",
      "landscape" : map (str, self.landscapes.all ()) if self.landscapes else "unknown",
      "can_flower" : "?" if self.can_flower is None else \
        "No" if self.can_flower is False else \
        "Yes (%s)" % map (str, self.flower.all ()),
      "can_fruit" : "?" if self.can_fruit is None else \
        "No" if self.can_fruit is False else \
        "Yes (%s)" % map (str, self.fruit.all ()),
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
