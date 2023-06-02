from flask import Flask
app = Flask(__name__)
from config import Config, ProductionConfig, DevelopmentConfig

#app.debug = True
if app.config['ENV']  == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config['ENV']  == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

from app import views