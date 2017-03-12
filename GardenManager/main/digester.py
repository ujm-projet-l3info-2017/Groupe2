#!/usr/bin/env python
# -*- coding: utf-8 -*-


import hashlib
import os


class Digester (object):

  """
    The Digester class allow the user to create a hash of a string using three
      phases:
        - the real hashing of the string ;
        - an encoding phase ;
        - a cutoff phase ;

    The algorithms used for theses phases are given by name like this:
      digester = Digester (name='-'.join (["sha256", "base64", "16"]))
      or
      digester = Digester (name="sha256-base64-16")
      The cutoff, hash_name and encoding can be given individualy by named
        parameter and are prevalant to the name:
      Digester (name="sha256-base64-90", hash_name=sha512) will use sha512.
      Digester (name="sha256-base64-16").digest ("some string") will apply the
        following algorithms to the given string (here: "some string"):
        - apply a sha256 to the string ;
        - convert it to base64 ;
        - cut the output to get a string with a maximum length of 16 characters.

    The user can provide a salt parameter equal to True, False, or any string.
    Default is False, it does not apply any salt.
    If True, a random (os.urandom) salt will be concatenated after the string to
      hash, before the hash phase (never the same salt). An additional parameter
      can be given: salt_length which is the length of the generated
      salt (default=16).
    If salt is a string, this string will be applied as the salt.

    If 0 is given as cutoff, there will not be any cutoff applied to the result.

    The suported hash algorithms are:
      hashlib.algorithms

    The supported encodings are:
      "base64", "", None
    You can add any encoding by doing
      Digester.SUPORTED_ENCODINGS.append (encoding)


    Examples of uses:
    sha256_base64_90 = Digester ()
    print sha256_base64_90.digest ("some string")
    regular_sha256 = Digester ("sha256;;")
    digester = Digester (hash_name="md5", cutoff=0, salt=True, salt_length=32)
    hashed, salt = digester.digest ("some string", get_salt=True)
    # lol, salt is bigger than output
  """

  HASH_ALGORITHMS = hashlib.algorithms
  SUPORTED_ENCODINGS = ["base64", "", None]
  SEP = ';'
  DEFAULT_HASH = "sha512"
  DEFAULT_ENCODING = "base64"
  DEFAULT_CUTOFF = "0"
  DEFAULT_NAME = SEP.join ([DEFAULT_HASH, DEFAULT_ENCODING,
    str (DEFAULT_CUTOFF)])

  def __init__ (self, name=DEFAULT_NAME, salt=False, salt_length=16,
      hash_name=None, cutoff=None, **kwargs):
    algo = name.split (Digester.SEP)
    if len (algo) != 3 and \
        (hash_name == None or encoding == None or cutoff == None):
      raise ValueError ("The digester name has not been recognized: '%s'" % \
        name)
    if hash_name is None:
      hash_name = algo[0]
    if kwargs.has_key ("encoding"):
      encoding = kwargs["encoding"]
    else:
      encoding = algo[1]
    if cutoff is None:
      cutoff = algo[2]
    if hash_name not in Digester.HASH_ALGORITHMS:
      raise ValueError ("The digester could not recognize the hash " + \
        "algorithm: '%s'" % hash_name)
    if encoding not in Digester.SUPORTED_ENCODINGS:
      raise ValueError ("The digester could not recognize the encoding: " \
        "'%s'" % encoding)
    try:
      self.cutoff = int (cutoff or 0)
    except ValueError:
      raise ValueError ("The given cutoff is not a integer: '%s'" % \
        str (cutoff))
    if not isinstance (salt_length, int):
      raise ValueError ("The salt length must be an int")
    if not salt_length >= 0:
      raise ValueError ("The salt length must be equal or more the 0")
    self.hash_algorithm = getattr (hashlib, hash_name)
    self.encoding = encoding
    self.salt_length = salt_length
    if salt is False:
      self.apply_salt = False
      self.salt = ""
    elif salt is True:
      self.apply_salt = True
      self.salt = None
    elif isinstance (salt, str):
      self.apply_salt = True
      self.salt = salt

  def digest (self, sentence="", get_salt=False):
    """
      This method apply the digest algorithm (hash, encode, cutoff) to the given
      string. If get_salt parameter is set to True, the output of this function
      is a tuple of two elements: (the result string, the salt used).
      Otherwise, just the string is returned.
    """
    hashed, salt = self.hash (sentence)
    encoded = self.encode (hashed).replace ("\n", "")
    result = self.cut (encoded)
    if get_salt:
      return result, salt
    return result

  def hash (self, sentence):
    """
      Apply the hash phase
    """
    if self.apply_salt and self.salt is None:
      salt = os.urandom (self.salt_length)
    else:
      salt = self.salt
    hashed = str (self.hash_algorithm (sentence + salt).digest ())
    return hashed, salt

  def encode (self, sentence):
    """
      Apply the encoding phase
    """
    return sentence.encode (self.encoding) if self.encoding else sentence

  def cut (self, sentence):
    """
      Apply the cutoff phase
    """
    if self.cutoff != 0:
      return sentence[:self.cutoff]
    return sentence


if __name__ == "__main__":
  help (Digester)

  d = Digester ()
  print d.digest ("test sentence")