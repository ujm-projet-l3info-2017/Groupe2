#!/usr/bin/env python
# -*- coding: utf-8 -*-


import scrapy


class GenusSpider (scrapy.Spider):

  name = "genus"

  def __init__ (self):
    super (GenusSpider, self).__init__ ()
    open ("genuses", "w").close ()

  base_url = "https://garden.org/plants/browse/plants/genus/?offset={}"
  start_urls = map (base_url.format, xrange (0, 16280, 20)) and []

  def parse (self, response):
    page = response.url.split ("/")[-2]
    with open ("genuses", "a") as f:
      genus = response.css ("div div div table tbody tr td a::text").extract ()
      f.write ('\n'.join (genus) + ('\n' if genus else ''))
