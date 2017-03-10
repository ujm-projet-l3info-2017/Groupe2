#!/usr/bin/env python
# -*- coding: utf-8 -*-


import scrapy


class URLSpider (scrapy.Spider):

  name = "URLSpider"

  def __init__ (self):
    super (URLSpider, self).__init__ ()
    open ("URLs", "w").close ()

  base_url = "https://plantdatabase.kpu.ca/"
  start_urls = [base_url + "plant/siteIndex"]
  #start_urls = map (base_url.format, xrange (0, 16280, 20)) and []

  def parse (self, response):
    with open ("URLs", "a") as f:
      urls = map (lambda x:x.xpath ("@href").extract (), response.xpath ("//tbody/tr/td/a"))
      #urls = response.css ("tbody tr td a.preview::href").extract ()
      print '\n'.join (map (lambda x:URLSpider.base_url + x[0], urls))
      f.write ('\n'.join (map (lambda x:URLSpider.base_url + x[0], urls)) + ('\n' if urls else ''))
