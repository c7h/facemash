import os
import sys
import site

basedir = os.path.abspath(os.path.dirname(__file__))
# Add the site-packages of the chosen virtualenv to work with
site.addsitedir(os.path.join(basedir, 'facemash/local/lib/python2.7/site-packages'))

# Add the app's directory to the PYTHONPATH
# sys.path.append('/home/django_projects/MyProject')
# sys.path.append('/home/django_projects/MyProject/myproject')

# Activate your virtual env
activate_env=os.path.expanduser(os.path.join(basedir, "facemash/bin/activate_this.py"))
execfile(activate_env, dict(__file__=activate_env))


import sys
from server import app

#Expand Python classes path with your app's path
sys.path.insert(0, os.path.join(basedir, "facemash"))

#Put logging code (and imports) here ...

#Initialize WSGI app object
application = app
