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
      "plant_type", "habit", "form", "height", 
      "spread", "growth_rate", "climate", "exposure", 
      "soil_or_growing_medium", "landscape_uses", "water",
      "leaf_colour_in_summer", "leaf_colour_in_fall", 
      "petal_colour", "flower_scent", "flower_time", "fruit_type", 
      "fruit_colour", "fruiting_time", "propagation" 
    }
  }

  ADDITIONNAL_KEYS = { key: set () for key in DATA_TYPES }
  ADDITIONNAL_KEYS["whole_plant"] = {
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
    self.csv_file = self.open_csv ()
    """
    try:
      self.process_raw_data (csv.DictReader (self.csv_file))
    except ValueError as error:
      raise error
    else:
      print "The given data has been processed successfully."
    finally:
      self.csv_file.close ()
    """
    self.process_raw_data (csv.DictReader (self.csv_file))
    self.csv_file.close ()

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

  def pass_mandatory_fields_tests (self, plant_data_set,
                                    data_type=DEFAULT_DATA_TYPE):
    """
     Takes a plant data set (a dictionnary) and search for missing mandatory
     keys.
    """
    missing_fields = Backend.MANDATORY_KEYS[data_type] - \
      set (plant_data_set.keys ())
    if not missing_fields:
      return None
    return "Missing fields: %s" % repr (sorted (list (missing_fields)))

  def process_tested_data (self, plant_data_set, data_type=DEFAULT_DATA_TYPE):
    """
      Insert the data into their respective table.
    """
    if data_type == "whole_plant":
      self.create_plant_and_related (plant_data_set)
    else:
      pass

  def create_model_instance (self, model_class, model_attributes):
    """
      Create an instance of the given model, having the given attributes
      and return the insgtance.
    """
    attributes = self.model_attributes.get (model_class, set ())
    arguments = dict (map (lambda key:(key, model_attributes[key]),
      set (attributes) & set (model_attributes)))
    instance = model_class.objects.get_or_create (**arguments)
    return instance[0]

  def create_plant (self, plant_data_set):
    """
      Create a models.Plant instance with the given data and return it.
    """
    self.sanitize_plant_data_set (plant_data_set)
    return self.create_model_instance (self.model_module.Plant, plant_data_set)

  def sanitize_plant_data_set (self, plant_data_set):
    print plant_data_set
    try:
      int (plant_data_set["climate"])
    except ValueError:
      search = re.search ("Zone (\w?\d+)", plant_data_set["climate"])
      climate_name = search and ("ZONE_" + search.groups ()[0]) or "ZONE_5"
      plant_data_set["climate"] = \
        self.model_module.Plant.CLIMATE_VALUE[str (climate_name)]
    try:
      int (plant_data_set["form"])
    except ValueError:
      plant_data_set["form"] = \
        self.model_module.Plant.FORM_VALUE[plant_data_set["form"].lower () or \
          "unknown"]
    try:
      int (plant_data_set["habit"])
    except ValueError:
      plant_data_set["habit"] = \
        self.model_module.Plant.HABIT_VALUE[plant_data_set["habit"].lower () or\
          "unknown"]
    try:
      int (plant_data_set["growth_rate"])
    except ValueError:
      plant_data_set["growth_rate"] = self.model_module.Plant.\
        GROWTH_RATE_VALUE[plant_data_set["growth_rate"].lower () or "unknown"]
    try:
      int (plant_data_set["water"])
    except ValueError:
      plant_data_set["water"] = self.model_module.Plant.WATER_VALUE[ \
        plant_data_set["water"].lower () or "unknown"]
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

  def create_landscape_uses (self, landscape_uses_data_set):
    """
      Create a models.LandscapeUses instance with the given data and return it.
    """
    print landscape_uses_data_set
    self.sanitize_landscape_data_set (landscape_uses_data_set)
    return self.create_model_instance (self.model_module.LandscapeUse, 
      landscape_uses_data_set)

  def sanitize_landscape_data_set (self, landscape_uses_data_set):
    if isinstance (landscape_uses_data_set["landscape"], str):
      landscape_uses_data_set["landscape"] = \
        self.model_module.LandscapeUse.LANDSCAPE_VALUES[\
          landscape_uses_data_set["landscape"]
        ]

  def parse_landscape_uses (self, landscape_uses):
    if landscape_uses.startswith ('"') and landscape_uses.endswith ('"') or \
        landscape_uses.startswith ("'") and landscape_uses.endswith ("'"):
      landscape_uses = landscape_uses[1:-1]
    landscape_uses = re.sub ("\ ?\([^)]*\)", "", landscape_uses)
    return re.split (",\ ?", landscape_uses)

  def create_plant_and_related (self, plant_data_set):
    plant = self.create_plant (plant_data_set)
    landscapes = self.create_landscape_use_set (plant_data_set)
    self.link_plant_to_landscapes (plant, landscapes)

  def create_landscape_use_set (self, plant_data_set):
    landscape_uses = plant_data_set.get ("landscape_uses", None)
    if landscape_uses is not None:
      uses = self.parse_landscape_uses (landscape_uses)
      return map (self.create_landscape_uses,
        map (lambda use: { "landscape": use }, uses))
    return []

  def link_plant_to_landscapes (self, plant, landscapes):
    print plant
    plant.landscapes.add (*landscapes)

  def open_csv (self):
    return open (self.args.csv[0], "rb")



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