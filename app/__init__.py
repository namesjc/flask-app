# import config
from flask import Flask

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = "/mnt/c/Users/cje5szh/Documents/project/flask-app/app/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]


# if app.config["ENV"] == "production":
#     app.config.from_object(config.ProductionConfig)
# else:
#     app.config.from_object(config.DevelopmentConfig)

from app import views, admin_views
