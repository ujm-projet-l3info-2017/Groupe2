#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os, sys
import csv
import argparse

import django
from django.conf import settings


class Backend (object):

  """
    Defines a backend class to be allowed to create some plant (for the moment)
    and its related tables.
    Only handle csv files for the moment.
  """

  SETTINGS_PATH = "GardenManager.settings"
  DATA_TYPES = "whole_plant", 
  DEFAULT_DATA_TYPE = "whole_plant"
  MANDATORY_KEYS = {
    "whole_plant": {
      "scientific_name", "common_name", "family_name", 
      "plant_type", "form", "height", 
      "spread", "growth_rate", "climate", "exposure", 
      "soil_or_growing_medium", "landscape_uses", "water",
      "leaf_colour_in_summer", "leaf_colour_in_fall", 
      "petal_colour", "flower_scent", "flower_time", "fruit_type", 
      "fruit_colour", "fruiting_time", "propagation" 
    }, 
    "plant": { "scientific_name", "common_name" },
    "landscape": { "landscape" },
    "climate": { "climate" },
    "exposure": { "exposure" },
    "water": { "water" },
    "ground": { "ground" },
    "form": { "form" },
    "habit": { "habit" },
    "month": { "month" },
    "fruit": { "fruit_type", "fruit_colour", "fruiting_time" },
    "colour": { "colour" },
    "fruit_type": { "type" }
  }

  ADDITIONNAL_KEYS = { key: set () for key in DATA_TYPES }
  ADDITIONNAL_KEYS["whole_plant"] = {
    "foreign_tables": dict (),
    "attributes": set ()
  }
  ADDITIONNAL_KEYS["plant"] = {
    "foreign_tables": {
      "Month": { "plantation_time" }
    }, "attributes": set ()
  }
  UNUSED_KEYS = { key: set () for key in DATA_TYPES }
  UNUSED_KEYS["whole_plant"]= {
    "pronunciation", "key_id_features", "texture", "origin", "additional_info",
    "leaf_form", "leaf_arrangement", "leaf_texture", "leaf_surfaces", 
    "leaf_shapes", "leaf_apices", "leaf_bases", "leaf_margins",
    "inflorescence_type", "bark_morphology", "bark_or_stem_colour",
    "pest_susceptibility"
  }

  @staticmethod
  def usable_arguments (args):
    """
      Return True if the arguments given in the command line are enough to
      execute one of the backend workflow.
    """
    return args.csv is not None

  def __init__ (self, args, settings_path=None):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
      settings_path or Backend.SETTINGS_PATH)
    django.setup ()
    self.args = args
    self.model_module = __import__ ("main").models
    model_module_attributes = dir (self.model_module)
    model_name_list = model_module_attributes[:model_module_attributes.index (\
      "__builtins__")]
    model_name_list.remove ("Digester")
    model_name_list.remove ("CircularList")
    self.models = {
      name: getattr (self.model_module, name) for name in model_name_list
    }
    self.model_attributes = {
      model: set (map (lambda x:x.name, model._meta.get_fields())) \
      for model in self.models.itervalues ()
    }

  def process_cmd_line (self):
    """
      Select the workflow to execute in function of the command arguments and
      execute it.
    """
    if self.args.csv is not None:
      self.process_csv ()

  def process_csv (self):
    """
      Process the csv file given in the command line
    """
    if os.path.exists (self.args.csv[0]) is False:
      raise ValueError ("The given path does not exists: '%s'." % \
        self.args.csv[0])
    with open (self.args.csv[0], "rb") as self.csv_file:
      self.process_raw_data (csv.DictReader (self.csv_file))
      print "The given data has been processed successfully."

  def process_raw_data (self, generator, data_type=DEFAULT_DATA_TYPE,
                        display_errors=True):
    """
      Wait for a list of dict objects having the keys predefined by the backend.
    """
    if hasattr (generator, "__iter__") is False:
      raise ValueError ("The given data are not iterable. Raw data has not" + \
        "been processed.")
    if data_type not in Backend.DATA_TYPES:
      raise ValueError ("Unknown data type: '%s'. Expected one of %s." % \
        (data_type, repr (Backend.DATA_TYPES)))
    errors = []
    for plant_data_set in generator:
      error = self.pass_mandatory_fields_tests (plant_data_set, data_type)
      if error is not None:
        errors.append (error)
      else:
        self.process_tested_data (plant_data_set, data_type)
    if display_errors is True:
      for error in errors:
        print >>sys.stderr, error

  def pass_mandatory_fields_tests (self, data_set,
      data_type=DEFAULT_DATA_TYPE):
    """
     Takes a data set (a dictionnary) and search for missing mandatory keys.
    """
    missing_fields = Backend.MANDATORY_KEYS[data_type] - data_set.viewkeys ()
    if not missing_fields:
      return None
    return "Missing fields: %s" % repr (sorted (list (missing_fields)))

  def process_tested_data (self, data_set, data_type=DEFAULT_DATA_TYPE):
    """
      Insert the data into their respective table.
    """
    if data_type == "whole_plant":
      self.create_plant_and_related (data_set)
    else:
      pass

  def create_model_instance (self, model_class, model_attributes):
    """
      Create an instance of the given model, having the given attributes
      and return the instance.
    """
    attributes = self.model_attributes.get (model_class, set ())
    arguments = dict (map (lambda key:(key, model_attributes[key]),
      set (attributes) & set (model_attributes)))
    instance = model_class.objects.get_or_create (**arguments)
    return instance[0]

  def split_from_data (self, sentence, sep=",\ ?", remove_parenthesis=True,
      remove_quotes=True, lower=True):
    """
      Split a sentence into a list of words/sub-sentences, using the regex sep.
      Strip the simple/double quotes from the original sentence if
        remove_quotes is True.
      Lower the sentence is lower is True (before split).
      Remove any parenthesis is remove_parenthesis is True (before split).
    """
    if remove_quotes:
      sentence = self.remove_trailing_from_data (sentence)
    try:
      while sentence is not None and remove_parenthesis and \
          sentence.index ('(') < sentence.index (')'):
        sentence = self.remove_parenthesis_from_data (sentence)
    except ValueError:
      pass
    if lower and sentence is not None:
      sentence = sentence.lower ()
    return re.split (sep, sentence or '')

  def remove_trailing_from_data (self, sentence, trailing="\"'"):
    for character in trailing:
      if sentence.startswith (character) and sentence.endswith (character):
        sentence = sentence[1:-1]
    return sentence

  def remove_parenthesis_from_data (self, sentence):
    return re.sub ("\ ?\([^)]*\)", "", sentence)

  def create_plant_and_related (self, plant_data_set):
    """
      Create a plant and all its related attributes in foreign tables:
        - exposures ;
        - flower (in progress) ;
        - forms ;
        - fruit (in progress) ;
        - grounds ;
        - habits ;
        - landscapes ;
        - waters ;
      The dataset is a dictionnary containing all {keys-value} for all tables.
    """
    plant = self.create_plant (plant_data_set, verify=False)
    exposures = self.create_exposure_set (plant_data_set, verify=False)
    forms = self.create_form_set (plant_data_set, verify=False)
    fruit = self.create_fruits (plant_data_set, verify=False)
    grounds = self.create_ground_set (plant_data_set, verify=False)
    habits = self.create_habit_set (plant_data_set, verify=False)
    landscapes = self.create_landscape_use_set (plant_data_set, verify=False)
    waters = self.create_water_set (plant_data_set, verify=False)
    self.link_plant_to_exposures (plant, exposures)
    self.link_plant_to_forms (plant, forms)
    self.link_plant_to_fruit (plant, fruit)
    self.link_plant_to_grounds (plant, grounds)
    self.link_plant_to_habits (plant, habits)
    self.link_plant_to_landscapes (plant, landscapes)
    self.link_plant_to_waters (plant, waters)
    print repr (plant)

  def create_plant (self, plant_data_set, verify=True):
    """
      Extract the plant's attributes from the plant_data_set,
      create a models.Plant instance with the given data and return it.
    """
    self.sanitize_plant_data_set (plant_data_set)
    additionnal_keys = Backend.ADDITIONNAL_KEYS.get ("plant", {})
    additionnal_attributes = additionnal_keys.get ("attributes", set ())
    additional_relations = additionnal_keys.get ("foreign_tables", dict ())
    plant = self.create_model_instance (self.model_module.Plant, plant_data_set)
    if additionnal_attributes:
      for attribute, value in additionnal_attributes.iteritems ():
        setattr (plant, attribute,  value)
    if additional_relations:
      for table_name in additional_relations.iterkeys ():
        self.process_tested_data (plant_data_set, data_type=table_name.lower ())
    return plant

  def sanitize_plant_data_set (self, plant_data_set):
    """
      Sanitize the plant's attributes from the dictionnary by:
        - Changing the climate value to its corresponding integer or
          Plant.DEFAULT_CLIMATE_NAME if unknown ;
        - Changing the growth rate value to its corresponding integer or
          "unknown" if not recognized ;
        - Create height_{min,max} from the height attribute ;
        - Create spread_{min,max} from the spread attribute.
    """
    try:
      int (plant_data_set["climate"])
    except ValueError:
      search = re.search ("Zone (\w?\d+)", plant_data_set["climate"])
      climate_name = search and ("ZONE_" + search.groups ()[0]) or \
        Plant.DEFAULT_CLIMATE_NAME
      plant_data_set["climate"] = \
        self.model_module.Plant.CLIMATE_VALUE[str (climate_name)]
    try:
      int (plant_data_set["growth_rate"])
    except ValueError:
      plant_data_set["growth_rate"] = self.model_module.Plant.\
        GROWTH_RATE_VALUE[plant_data_set["growth_rate"].lower () or "unknown"]
    if plant_data_set.has_key ("height_min") is False:
      search = re.search ("(\d+(\.\d+)?)\ \-", plant_data_set["height"])
      if search is not None:
        plant_data_set["height_min"] = float (search.groups ()[0])
    if plant_data_set.has_key ("height_max") is False:
      search = re.search ("\ \-\ (\d+(\.\d+)?)", plant_data_set["height"])
      if search is not None:
        plant_data_set["height_max"] = float (search.groups ()[0])
    if plant_data_set.has_key ("spread_min") is False:
      search = re.search ("(\d+(\.\d+)?)\ \-", plant_data_set["spread"])
      if search is not None:
        plant_data_set["spread_min"] = float (search.groups ()[0])
    if plant_data_set.has_key ("spread_max") is False:
      search = re.search ("\ \-\ (\d+(\.\d+)?)", plant_data_set["spread"])
      if search is not None:
        plant_data_set["spread_max"] = float (search.groups ()[0])

  def link_plant_to_exposures (self, plant, exposures):
    plant.exposures.add (*exposures)

  def link_plant_to_forms (self, plant, forms):
    plant.forms.add (*forms)

  def link_plant_to_fruit (self, plant, fruit):
    if fruit:
      plant.fruit = fruit

  def link_plant_to_grounds (self, plant, grounds):
    plant.grounds.add (*grounds)

  def link_plant_to_habits (self, plant, habits):
    plant.habits.add (*habits)

  def link_plant_to_landscapes (self, plant, landscapes):
    plant.landscapes.add (*landscapes)

  def link_plant_to_waters (self, plant, waters):
    plant.waters.add (*waters)

  def create_fruits (self, fruit_data_set, verify=True):
    """
      Extract the fruit's attributes from the fruit_data_set,
      create a models.Fruit instance with the given data.
      Create the related months and link them to the created fruit.
      Return the newly created fruit.
    """
    self.sanitize_fruit_data_set (fruit_data_set)
    errors = self.pass_mandatory_fields_tests (fruit_data_set, "fruit")
    assert errors is None, errors
    fruit = self.create_model_instance (self.model_module.Fruit, fruit_data_set)
    months = self.create_month_set (
      {"months" : fruit_data_set["fruiting_time"]})
    colours = self.create_colour_set (
      {"colours" : fruit_data_set["fruit_colour"]})
    types = self.create_fruit_type_set (
      {"types" : fruit_data_set["fruit_type"]})
    self.link_fruit_to_months (fruit, months)
    self.link_fruit_to_colours (fruit, colours)
    self.link_fruit_to_types (fruit, types)
    
    return fruit

  def sanitize_fruit_data_set (self, fruit_data_set):
    """
      Sanitize the fruit_data_set dictionnary by:
        - Replacing the fruit value by its corresponding integer.
    """
    return

  def link_fruit_to_months (self, fruit, months):
    fruit.months.add (*months)

  def link_fruit_to_colours (self, fruit, colours):
    fruit.colours.add (*colours)

  def link_fruit_to_types (self, fruit, types):
    fruit.types.add (*types)

  def create_fruit_types (self, fruit_type_data_set, verify=True):
    """
      Extract the fruit_type's attributes from the fruit_type_data_set,
      create a models.FruitType instance with the given data and return it.
    """
    self.sanitize_fruit_type_data_set (fruit_type_data_set)
    errors = self.pass_mandatory_fields_tests (fruit_type_data_set, "fruit_type")
    assert errors is None, errors
    return self.create_model_instance (self.model_module.FruitType, 
      fruit_type_data_set)

  def parse_fruit_types (self, fruit_type):
    """
      Extract all diffrent fruit_types (without parenthesis) from comma
      separated sentence.
    """
    return self.split_from_data (fruit_type, lower=True)

  def sanitize_fruit_type_data_set (self, fruit_type_data_set):
    """
      Sanitize the fruit_type_data_set dictionnary by:
        - Replacing the fruit_type value by its corresponding integer.
    """
    if isinstance (fruit_type_data_set["fruit_type"], str):
      fruit_type_data_set["fruit_type"] = self.model_module.FruitType.\
        TYPE_VALUES[fruit_type_data_set["fruit_type"] or "unknown"]

  def create_fruit_type_set (self, fruit_type_data_set, verify=True):
    fruit_types = fruit_type_data_set.get ("fruit_type", None)
    if fruit_types is not None:
      fruit_types = self.parse_fruit_types (fruit_types)
      return map (lambda *args:self.create_fruit_types (*args, verify=verify),
        map (lambda fruit_type: { "fruit_type": fruit_type }, fruit_types))
    return []

  def create_exposures (self, exposure_data_set, verify=True):
    """
      Extract the exposure's attributes from the exposure_data_set,
      create a models.Exposure instance with the given data and return it.
    """
    self.sanitize_exposure_data_set (exposure_data_set)
    errors = self.pass_mandatory_fields_tests (exposure_data_set, "exposure")
    assert errors is None, errors
    return self.create_model_instance (self.model_module.Exposure, 
      exposure_data_set)

  def parse_exposures (self, exposure):
    """
      Extract all diffrent exposures (without parenthesis) from comma
      separated sentence.
    """
    return self.split_from_data (exposure, lower=True)

  def sanitize_exposure_data_set (self, exposure_data_set):
    """
      Sanitize the exposure_data_set dictionnary by:
        - Replacing the exposure value by its corresponding integer.
    """
    if isinstance (exposure_data_set["exposure"], str):
      exposure_data_set["exposure"] = self.model_module.Exposure.\
        EXPOSURE_VALUES[exposure_data_set["exposure"] or "unknown"]

  def create_exposure_set (self, exposure_data_set, verify=True):
    exposures = exposure_data_set.get ("exposure", None)
    if exposures is not None:
      exposures = self.parse_exposures (exposures)
      return map (lambda *args:self.create_exposures (*args, verify=verify),
        map (lambda exposure: { "exposure": exposure }, exposures))
    return []

  def create_forms (self, form_data_set, verify=True):
    """
      Extract the form's attributes from the form_data_set,
      create a models.Form instance with the given data and return it.
    """
    self.sanitize_form_data_set (form_data_set)
    errors = self.pass_mandatory_fields_tests (form_data_set, "form")
    assert errors is None, errors
    return self.create_model_instance (self.model_module.Form, 
      form_data_set)

  def parse_forms (self, form):
    """
      Extract all diffrent forms (without parenthesis) from comma
      separated sentence.
    """
    return self.split_from_data (form, lower=True)

  def sanitize_form_data_set (self, form_data_set):
    """
      Sanitize the form_data_set dictionnary by:
        - Replacing the form value by its corresponding integer.
    """
    if isinstance (form_data_set["form"], str):
      form_data_set["form"] = \
        self.model_module.Form.FORM_VALUES[form_data_set["form"] or "unknown"]

  def create_form_set (self, form_data_set, verify=True):
    forms = form_data_set.get ("form", None)
    if forms is not None:
      forms = self.parse_forms (forms)
      return map (lambda *args:self.create_forms (*args, verify=verify),
        map (lambda form: { "form": form }, forms))
    return []

  def create_grounds (self, ground_data_set, verify=True):
    """
      Extract the ground's attributes from the ground_uses_data_set,
      create a models.Ground instance with the given data and return it.
    """
    self.sanitize_ground_data_set (ground_data_set)
    errors = self.pass_mandatory_fields_tests (ground_data_set, "ground")
    assert errors is None, errors
    return self.create_model_instance (self.model_module.Ground, 
      ground_data_set)

  def parse_grounds (self, ground):
    """
      Extract all diffrent grounds (without parenthesis) from comma
      separated sentence.
    """
    return self.split_from_data (ground, lower=True)

  def sanitize_ground_data_set (self, ground_data_set):
    """
      Sanitize the ground_data_set dictionnary by:
        - Replacing the ground value by its corresponding integer.
    """
    if isinstance (ground_data_set["ground"], str):
      ground_data_set["ground"] = self.model_module.Ground.GROUND_VALUES[\
        ground_data_set["ground"] or "unknown"]

  def create_ground_set (self, ground_data_set, verify=True):
    grounds = ground_data_set.get ("soil_or_growing_medium", None)
    if grounds is not None:
      grounds = self.parse_grounds (grounds)
      return map (lambda *args:self.create_grounds (*args, verify=verify),
        map (lambda ground: { "ground": ground }, grounds))
    return []

  def create_habits (self, habit_data_set, verify=True):
    """
      Extract the habit's attributes from the habit_data_set,
      create a models.Habit instance with the given data and return it.
    """
    self.sanitize_habit_data_set (habit_data_set)
    errors = self.pass_mandatory_fields_tests (habit_data_set, "habit")
    assert errors is None, errors
    return self.create_model_instance (self.model_module.Habit, 
      habit_data_set)

  def parse_habits (self, habit):
    return self.split_from_data (habit)

  def sanitize_habit_data_set (self, habit_data_set):
    """
      Sanitize the habit_data_set dictionnary by:
        - Replacing the habit value by its corresponding integer.
    """
    if isinstance (habit_data_set["habit"], str):
      habit_data_set["habit"] = self.model_module.Habit.HABIT_VALUES[\
        habit_data_set["habit"] or "unknown"]

  def create_habit_set (self, habit_data_set, verify=True):
    habits = habit_data_set.get ("habit", None)
    if habits is not None:
      habits = self.parse_habits (habits)
      return map (lambda *args: self.create_habits (*args, verify=verify),
        map (lambda habit: { "habit": habit }, habits))
    return []

  def create_landscape_uses (self, landscape_uses_data_set, verify=True):
    """
      Extract the landscape's attributes from the landscape_uses_data_set,
      create a models.LandscapeUses instance with the given data and return it.
    """
    self.sanitize_landscape_data_set (landscape_uses_data_set)
    errors = self.pass_mandatory_fields_tests (landscape_uses_data_set, \
      "landscape")
    assert errors is None, errors
    return self.create_model_instance (self.model_module.LandscapeUse, 
      landscape_uses_data_set)

  def sanitize_landscape_data_set (self, landscape_uses_data_set):
    """
      Sanitize the landscape_uses_data_set dictionnary by:
        - Replacing the landscape value by its corresponding integer.
    """
    if isinstance (landscape_uses_data_set["landscape"], str):
      landscape_uses_data_set["landscape"] = \
        self.model_module.LandscapeUse.LANDSCAPE_VALUES[\
          landscape_uses_data_set["landscape"] or "unknown"
        ]

  def parse_landscape_uses (self, landscape_uses):
    return self.split_from_data (landscape_uses, lower=False)

  def create_landscape_use_set (self, plant_data_set, verify=True):
    landscape_uses = plant_data_set.get ("landscape_uses", None)
    if landscape_uses is not None:
      uses = self.parse_landscape_uses (landscape_uses)
      return map (lambda *args:self.create_landscape_uses(*args, verify=verify),
        map (lambda use: { "landscape": use }, uses))
    return []

  def create_colour (self, colour_data_set, verify=True):
    """
      Extract the colour's attributes from the colour_data_set,
      create a models.Colour instance with the given data.
    """
    self.sanitize_colour_data_set (colour_data_set)
    if colour_data_set["colour"] is not None:
      errors = self.pass_mandatory_fields_tests (colour_data_set, "colour")
      assert errors is None, errors
      return self.create_model_instance (self.model_module.Colour, colour_data_set)

  def parse_colours (self, colour):
    """
      Extract all diffrent colours (without parenthesis) from comma
      separated sentence.
    """
    return self.split_from_data (colour, lower=True)

  def sanitize_colour_data_set (self, colour_data_set):
    """
      Sanitize the colour_data_set dictionnary by:
        - Replacing the colour value by its corresponding integer.
    """
    if isinstance (colour_data_set["colour"], str):
      if colour_data_set["colour"] in ("n/a", '', None):
        colour_data_set["colour"] = "unknown"
      colour_data_set["colour"] = self.model_module.Colour.COLOUR_VALUES[\
        colour_data_set["colour"]]

  def create_colour_set (self, colour_data_set, verify=True):
    colours = colour_data_set.get ("colours", None)
    if colours is not None:
      colours = self.parse_colours (colours)
      return filter (None, map (lambda *args:self.create_colour (*args,
        verify=verify), map (lambda colour: { "colour": colour }, colours)))
    return []

  def create_month (self, month_data_set, verify=True):
    """
      Extract the month's attributes from the month_data_set,
      create a models.Month instance with the given data.
    """
    self.sanitize_month_data_set (month_data_set)
    if month_data_set["month"] is not None:
      errors = self.pass_mandatory_fields_tests (month_data_set, "month")
      assert errors is None, errors
      return self.create_model_instance (self.model_module.Month, month_data_set)

  def parse_months (self, month):
    """
      Extract all diffrent months (without parenthesis) from comma
      separated sentence.
    """
    return self.split_from_data (month, lower=True)

  def sanitize_month_data_set (self, month_data_set):
    """
      Sanitize the month_data_set dictionnary by:
        - Replacing the month value by its corresponding integer.
    """
    if isinstance (month_data_set["month"], str):
      if month_data_set["month"] in ("n/a", '', None):
        month_data_set["month"] = None
      else:
        month_data_set["month"] = self.model_module.Month.MONTH_VALUES[\
          self.model_module.Month.MONTH_FULL_NAME[month_data_set["month"]]]

  def create_month_set (self, month_data_set, verify=True):
    months = month_data_set.get ("months", None)
    if months is not None:
      months = self.parse_months (months)
      return filter (None, map (lambda *args:self.create_month (*args,
        verify=verify), map (lambda month: { "month": month }, months)))
    return []

  def create_waters (self, water_data_set, verify=True):
    """
      Extract the water's attributes from the warer_data_set,
      create a models.Water instance with the given data and return it.
    """
    self.sanitize_water_data_set (water_data_set)
    errors = self.pass_mandatory_fields_tests (water_data_set, "water")
    assert errors is None, errors
    return self.create_model_instance (self.model_module.Water, 
      water_data_set)

  def parse_waters (self, water):
    """
      Extract all diffrent waters (without parenthesis) from comma
      separated sentence.
    """
    return self.split_from_data (water, lower=True)

  def sanitize_water_data_set (self, water_data_set):
    """
      Sanitize the water_data_set dictionnary by:
        - Replacing the water value by its corresponding integer.
    """
    if isinstance (water_data_set["water"], str):
      water_data_set["water"] = \
        self.model_module.Water.WATER_VALUES[water_data_set["water"] or \
          "unknown"]

  def create_water_set (self, water_data_set, verify=True):
    waters = water_data_set.get ("water", None)
    if waters is not None:
      waters = self.parse_waters (waters)
      return map (lambda *args:self.create_waters (*args, verify=verify),
        map (lambda water: { "water": water }, waters))
    return []



if __name__ == "__main__":

  description = "A backend script to fill the database with some data.\n" + \
    "Only CSV files can be used for the moment."
  parser = argparse.ArgumentParser (description=description)
  parser.add_argument ('--csv', metavar='csv_path', type=str, nargs=1,
    help='The path to the CSV file to process')

  args = parser.parse_args ()

  if Backend.usable_arguments (args) is False:
    #backend = Backend (args=args)
    parser.print_help ()
    exit ()

  backend = Backend (args=args)
  backend.process_cmd_line ()

  exit ()