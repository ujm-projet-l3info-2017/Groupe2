#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
  I needed a circular list to get (for example) some months from novembre to
  february.
  So, instead of doing:
  $ months[11:] + months[:3]
  I'll do
  $ months[11:15]
  it's better. It does not worth the work, but I love doing this kind of thing,
  and in fact, it can heavily be reused.
"""


class CircularList (object):

  """
    A circular list has no end. In one try to get an item at an index greater
    than the list's item number, the index act like it continues its path from
    the begining of the list.
  """

  def __init__ (self, iterable=None, max_length=None):
    self.real_list = list (iterable or ())
    if max_length is not None:
      if not isinstance (max_length, int):
        raise TypeError ("max_length type must be int or NoneType.")
      if max_length < 0:
        raise ValueError ("max_length cannot be less than 0.")
      if len (self.real_list) > max_length:
        self.real_list = self.real_list[len (self.real_list)-max_length:]
    self.max_length = max_length

  def __add__ (self, iterable):
    iter (iterable)
    return CircularList (iterable=self.real_list+list (iterable),
      max_length=self.max_length)

  def __contains__ (self, item):
    return item in self.real_list

  def __delitem__ (self, index):
    length = len (self.real_list)
    if length == 0:
      raise IndexError ("list index out of range")
    del self.real_list[index % length]

  def __delslice__ (self, start, end):
    if end - start > 0:
      length = len (self.real_list)
      if end - start < length:
        self.real_list = self.real_list[:start % length] + \
          self.real_list[end % length:]
      else:
        self.real_list[:] = []

  def __eq__ (self, iterable):
    try:
      iter (iterable)
    except TypeError:
      return False
    return list (iterable) == self.real_list

  def __ge__ (self, iterable):
    try:
      iter (iterable)
    except TypeError:
      return False
    return list (iterable) >= self.real_list

  def __getitem__ (self, item_slice):
    def CircularList (item_slice):
      if self.max_length == 0:
        raise StopIteration ()
      if isinstance (item_slice, int):
        yield self.real_list[item_slice % len (self.real_list)]
        raise StopIteration ()
      start, stop, step = map (item_slice.__getattribute__,
        ["start", "stop", "step"])
      if step is None:
        step = 1 if stop > start else -1
      if not isinstance (start, int):
        raise TypeError ("start must be int, not %s" % type (start))
      if not isinstance (stop, int):
        raise TypeError ("stop must be int, not %s" % type (stop))
      if step == 0 or \
          (start > stop and step > 0) or \
          (start < stop and step < 0):
        raise StopIteration ()
      while start != stop:
        yield self.real_list[start % len (self.real_list)]
        start += step
    return CircularList (item_slice)

  def __getslice__ (self, start, stop):
    return self[start:stop:1 if stop > start else -1]

  def __ge__ (self, iterable):
    try:
      iter (iterable)
    except TypeError:
      return False
    return list (iterable) > self.real_list

  def __iadd__ (self, iterable):
    self.real_list = (self.real_list + list (iterable))[-self.max_length:]

  def __imul__ (self, value):
    if not isinstance (value, int):
      raise TypeError ("Can only multiply CircularList with int")

  def __iter__ (self):
    return iter (self.real_list)

  def __le__ (self, iterable):
    try:
      iter (iterable)
    except TypeError:
      return False
    return list (iterable) <= self.real_list

  def __len__ (self):
    return len (self.real_list)

  def __lt__ (self, iterable):
    try:
      iter (iterable)
    except TypeError:
      return False
    return list (iterable) < self.real_list

  def __mul__ (self, value):
    if not isinstance (value, int):
      raise TypeError ("Can only multiply CircularList with int")
    return CircularList (self.real_list, self.max_length)

  def __ne__ (self, iterable):
    try:
      iter (iterable)
    except TypeError:
      return False
    return list (iterable) != self.real_list

  def __repr__ (self):
    return "<CircularList object at 0x%x>" % id (self)

  def __reversed__ (self):
    return CircularList (reversed (self.real_list), self.max_length)

  def __rmul__ (self, value):
    return self * value

  def __setitem__ (self, index, item):
    if self.max_length is None or self.max_length != 0:
      length = len (self.real_list)
      if length != 0:
        self.real_list[index % length] = item

  def __setslice__ (self, start, end, item):
    if end - start > 0:
      length = len (self.real_list)
      try:
        item = list (item)
      except TypeError:
        item = [item]
      if end - start < length:
        self.real_list = self.real_list[:start % length] + item + \
          self.real_list[end % length:]
      else:
        self.real_list[:] = item

  def __str__ (self):
    if self.max_length != 0 and len (self.real_list) != 0:
      return "[..., %s, ...]" % str (self.real_list)[1:-1]
    return "[...]"

  def append (self, item):
    self.real_list.append (item)
    if self.max_length is not None and self.max_length != 0:
      del self.real_list[0]

  def count (self, item):
    return self.real_list.count (item)

  def extend (self, item):
    self.real_list.extend (item)
    if self.max_length is not None and self.max_length != 0:
      del self.real_list[-1]

  def index (self, value, start=0, stop=None):
    if stop > self.max_length:
      stop = self.max_length
    else:
      length = len (self.real_list)
      if stop > length:
        stop = length
    return list (self[start:stop]).index (value)

  def pop (self):
    if len (self.real_list):
      return self.real_list.pop ()

  def remove (self, value):
    return self.real_list.remove (value)

  def reverse (self):
    self.real_list = self.real_list[::-1]

  def sort (self, cmp=None, key=None, reverse=False):
    self.real_list.sort (cmp=cmp, key=key, reverse=reverse)



if __name__ == "__main__":
  assert list (CircularList (range(14), 5)[14:1:-1]) == [13, 12, 11, 10, 9, 13, 12, 11, 10, 9, 13, 12, 11]
  assert CircularList (range(14), 5)[1:14:1]
  assert CircularList (range(14), 5)[1:]
  assert list (CircularList (range (10))) == range (10)
  s = CircularList (range (10))
  assert list (s[1473]) == [3]
  s.append (10)
  assert list (s[1473:1493]) == [10] + range (11) + range(8)
  assert str (s) == "[..., 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]"