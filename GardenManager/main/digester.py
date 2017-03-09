#!/usr/bin/env python
# -*- coding: utf-8 -*-


import hashlib
import os


class Digester ():

  PRIMARY = set (hashlib.algorithms)
  SECONDARY = set (["base64", "ascii", "utf8", ""])

  def __init__ (self, name="sha512-base64-90", salt=False, salt_length=16):
    algo = name.split ('-')
    if len (algo) != 3:
      raise ValueError ("The digester name has not been recognized: '%s'" % \
        name)
    if algo[0] not in Digester.PRIMARY:
      raise ValueError ("The digester could not recognize the hash " + \
        "algorithm: '%s'" % algo[0])
    if algo[1] not in Digester.SECONDARY:
      raise ValueError ("The digester could not recognize the coding: '%s'" % \
        algo[1])
    try:
      self.cutoff = int (algo[2])
    except ValueError:
      raise ValueError ("The given cutoff is not a number: '%s'" % algo[2])
    self.hash_algorithm = getattr (hashlib, algo[0])
    self.encoding = algo[1]
    if salt is False:
      self.salt = ""
    elif salt is True:
      self.salt = os.urandom (salt_length)

  def digest (self, sentence, get_salt=False):
    hashed = self.hash (sentence)
    encoded = self.encode (hashed)
    result = self.cut (encoded)
    if get_salt:
      return result, self.salt
    return result

  def hash (self, sentence):
    return str (self.hash_algorithm (sentence + self.salt).digest ())

  def encode (self, sentence):
    return sentence.encode (self.encoding)

  def cut (self, sentence):
    if self.cutoff != 0:
      return sentence[:self.cutoff]
    return sentence
