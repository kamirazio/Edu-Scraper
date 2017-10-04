import os, sys
import logging

logging.basicConfig(stream=sys.stderr)
PROJECT_DIR = '/var/www/html/ted_spider/'

activate_this = os.path.join(PROJECT_DIR, 'bin', 'ac:wqtivate_this.py')
execfile(activate_this, dict(__file__=activate_this))
sys.path.append(PROJECT_DIR)

from flask import app as application
