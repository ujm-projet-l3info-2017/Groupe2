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