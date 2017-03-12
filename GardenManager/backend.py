#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
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
      "spread", "growth_rate", "hardiness_rating", "exposure", 
      "soil_or_growing_medium", "landscape_uses", 
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
    if os.path.exists (self.args.csv) is False:
      raise ValueError ("The given path does not exists: '%s'." % \
        self.args.csv)
    self.csv_file = self.open_csv ()
    try:
      self.process_raw_data (csv.DictReader (csv_file))
    except ValueError as error:
      raise error
    else:
      print "The given data has been processed successfully."
    finally:
      self.csv_file.close ()

  def process_raw_data (self, generator, data_type=DATA_TYPES):
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

  def pass_mandatory_fields_tests (self, plant_data_set, data_type=DATA_TYPES):
    """
     Takes a plant data set (a dictionnary) and search for missing mandatory
     keys.
    """
    missing_fields = Backend.MANDATORY_KEYS[data_type] - \
      set (plant_data_set.keys ())
    if not missing_fields:
      return None
    return "Missing fields: %s" % repr (list (missing_fields))

  def process_tested_data (self, plant_data_set, data_type=DATA_TYPES):
    """
      Insert the data into their respective table.
    """
    pass #lol

  def open_csv (self):
    return open (self.args.csv, "rb")



if __name__ == "__main__":

  description = "A backend script to fill the database with some data.\n" + \
    "Only CSV files can be used for the moment."
  parser = argparse.ArgumentParser (description=description)
  parser.add_argument ('--csv', metavar='csv_path', type=str, nargs=1,
    help='The path to the CSV file to process')
  args = parser.parse_args ()
  if Backend.usable_arguments (args) is False:
    parser.print_help ()
    exit ()
  backend = Backend (args=args)
  backend.process_cmd_line ()
  exit ()