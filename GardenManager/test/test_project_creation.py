#!/usr/bin/env python

import os


os.chdir ("..")

params = {
  "project_name": "balto_test_project",
  "user": "balto",
  "area_number": 3,
  "soil_type": 4, # humus rich
  "area_1_point_number": 4,
  "area_2_point_number": 4,
  "area_3_point_number": 3,
}

os.system ("""echo 'balto_test_project\nbalto\n3\n4\n4\n'""")
os.system ("""echo '%(project_name)s
%(user)s
%(area_number)d
%(soil_type)d
%(area_1_point_number)d
0:0
5:0
5:5
0:5
%(soil_type)d
%(area_2_point_number)d
5:0
10:0
10:5
5:5
%(soil_type)d
%(area_3_point_number)d
0:5
10:5
5:10
' | ./backend.py --project-creation 1""" % params)
