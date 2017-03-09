#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GardenManager.settings")


class Backend (object):

  def __init__ (self, models):
    self.models = models


django.setup ()

from main import models


if __name__ == "__main__":
  Backend (models)