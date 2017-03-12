#!/usr/bin/env python
# -*- coding: utf-8 -*-


import scrapy
import csv
import re


class PlantSpider (scrapy.Spider):

  name = "PlantSpider"

  with open ("URLs", "r") as f:
    start_urls = map (str.strip, f.readlines ())

  def __init__ (self):
    super (PlantSpider, self).__init__ ()
    self.header = map (unicode, [
      "scientific_name", "pronunciation", "common_name", "family_name",
      "plant_type", "key_id_features",
      "habit", "form", "texture", "height", "spread", "growth_rate", "origin",
      "climate", "exposure", "soil_or_growing_medium", "water_use", 
      "landscape_uses",
      "additional_info", "leaf_form", "leaf_arrangement",
      "leaf_texture", "leaf_surfaces", "leaf_colour_in_summer", "leaf_colour_in_fall", "leaf_shapes",
      "leaf_apices", "leaf_bases", "leaf_margins",
      "inflorescence_type", "petal_colour", "flower_scent", "flower_time",
      "fruit_type", "fruit_colour", "fruiting_time",
      "bark_morphology", "bark_or_stem_colour", "propagation",
      "pest_susceptibility"])
    self.csvfile = open('plantes.csv', 'w')
    self.writer = csv.DictWriter(self.csvfile, fieldnames=self.header)
    self.writer.writeheader()
    self.replacement = {
      "soil/_growing_medium": "soil_or_growing_medium",
      "leaf_texture/_venation": "leaf_texture",
      "flower_flower_scent": "flower_scent",
      "flower_flower_time": "flower_time",
      "flower_colour_(petals)": "petal_colour",
      "flower_flower_time_at_peak": "flower_time",
      "hardiness_rating": "climate"
    }
    self.frames = {
      "leaf_morphology": "leaf",
      "flower_morphology": "flower",
      "flower_morphology": "flower",
    }

  def parse (self, response):
    rows = {}
    tds = response.xpath ("//tr/td")
    skip = None
    frame = None
    for no, td in enumerate (tds):
      if no == skip:
        no = None
        continue
      key = '_'.join (filter (lambda x:x!='', map (self.trim, td.xpath (".//text()").extract ())))
      if key:
        if self.frames.has_key (key):
          frame = self.frames[key]
          continue
        if frame is not None:
          key = frame + "_" + key
          if key in ("leaf_margins", "flower_flower_time_at_peak"):
            frame = None
        if self.replacement.has_key (key):
          key = self.replacement[key]
        if key in self.header:
          value = tds[no+1].xpath (".//text()").extract ()
          skip = no + 1
          rows[key] = ' '.join (filter (lambda x:x!='', map (self.trim_no_under, value)))
        else:
          pass#print key
    self.writer.writerow ({key.encode ("utf-8"): value.encode ("utf-8") for key, value in rows.iteritems ()})

  def trim_no_under (self, text):
    return self.trim (text, False)

  def trim (self, text, underscore=True):
    trimed = re.sub (":$", '', re.sub ("[\n\r\t\ ]+", " ", text).strip ())
    if underscore:
      trimed = trimed.lower ().replace (" ", "_")
    return trimed