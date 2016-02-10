import os

from flask import Flask
from playhouse.flask_utils import FlaskDB

# Configuration values.
APP_DIR = os.path.dirname(os.path.realpath(__file__))

# The playhouse.flask_utils.FlaskDB object accepts database URL configuration.
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'permanote2.db')
# Version for Sandstorm TODO make this work in both dev and prod
# DATABASE = 'sqliteext:////var/permanote2.db'
DEBUG = True

application = Flask(__name__)
application.config.from_object(__name__)

# FlaskDB is a wrapper for a peewee database that sets up pre/post-request
# hooks for managing database connections.
flask_db = FlaskDB(application)

# The `database` is the actual peewee database, as opposed to flask_db which is
# the wrapper.
database = flask_db.database

# Upload folder and file allowed extensions
# for sandstorm TODO make this work in both dev and prod
# application.config['UPLOAD_FOLDER'] = '/var/uploads'
# for development
application.config['UPLOAD_FOLDER'] = '/home/tom/Development/permanote2/uploads'

# file types allowed for upload
application.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'png', 'gif'])

# This is used by micawber, which will attempt to generate rich media
# embedded objects with maxwidth=800.
application.config['SITE_WIDTH'] = 800

# The secret key is used internally by Flask to encrypt session data stored
# in cookies. Make this unique for your app.
application.config['SECRET_KEY'] = 'asdfkj23kjdflkj23lkjs'
