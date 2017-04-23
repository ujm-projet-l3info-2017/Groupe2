Garden Project
==============



Metadata
--------

 * **@name**: Garden Project
 * **@version**: 1.0
 * **@authors**: PAVOT Baltazar ; PELEGRIN Romain ; RIGHI Sarah
 * **@date creation**: 2017/02/14
 * **@main usage**: Website to manage your gardens.


Developer info
------------------
Some commit hook have been set.
Put this text into .git/hooks/commit-msg:
```python
#!/usr/bin/env python


import sys
import re


if __name__ == "__main__":

  if len (sys.argv) != 2:
    print >> sys.stderr, "You must give the commit file as first argument"
    exit (1)

  regexps = [
    "^(feat|fix|docs|style|refactor|test|chore)\(.+\)\:\ .+$",
    "^$",
    "^.+$"
  ]

  with open (sys.argv[1], "r") as commit_file:
    lines = commit_file.readlines ()

  if len (lines) < 3:
    print >> sys.stderr, "Bad global pattern: There must be at least 3 lines."
    exit (1)

  for no, (line, regexp) in enumerate (zip (lines, regexps)):
    if re.match (regexp, line) is None:
      print >> sys.stderr, "Bad pattern at line %d:\n'%s'\n%s" % (no+1,
        line.replace ("\n", ""), regexp)
      exit (1)

  exit (0)
```
Put this text into .git/commit.sample: 
```text
<type>(<scope>): <subject>

<body>

<optionnal_footer>
```
Open a terminal in the parent directory
of .git then type
```bash
git config commit.template .git/commit.template
```
Keep following the sample not to be rejected by hooks.



Configuration
-------------

### Requirement:
 * Debian

Install pip
```bash
sudo apt-get install python-pip
```
Install django
```bash
sudo pip install django
```


### Deploy:

 * Getting the project ready to work

```bash
git clone git@github.com:ujm-projet-l3info-2017/Groupe2.git
  # ou 
git clone https://github.com/ujm-projet-l3info-2017/Groupe2.git
```

 * Launch the application

```bash
git checkout master
cd GardenManager
python ./manage.py runserver
```


Technical description
---------------------
Developed under python 2.7 and django 1.10.6


Notes
-----------
If the application is hosted on your onw computer, to access it, launch it then
go to 127.0.0.1:3000 on your web browser.