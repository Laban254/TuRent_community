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

UPLOAD_FOLDER = '/app/house_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024



from app import views