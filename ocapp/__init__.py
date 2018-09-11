#from flask import Flask
##from config import Config
#
#from .views import app
#from . import controllers
#
#app = Flask(__name__)
##app.config.from_object(Config)
#
#from ocapp import views

from flask import Flask

from .views import app
from . import controllers