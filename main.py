import os
from flask import Flask,render_template
from flask_session import Session
from flask_restful import Api
from flask_login import LoginManager
from application.confix import LocalDevelopmentConfig
from application.models import db

def create_app(app=None):


    app= Flask(__name__,static_folder="static",template_folder="templates")
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    if os.getenv('ENV',"development") == "production":
        raise Exception("No production config setup")
    else:
        print("Starting local development")
        app.config.from_object(LocalDevelopmentConfig)
    
    db.init_app(app) 
    api=Api(app)   
  
    app.app_context().push()
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app,api

app,api = create_app()

from application.controllers import *

from application.api import ProductApi,AdminApi,CategoryApi

# # mapping Apiclass to respective paths
api.add_resource(ProductApi,"/api/product/<string:name>","/api/product")
api.add_resource(CategoryApi,"/api/category/<string:name>","/api/category")
api.add_resource(AdminApi,"/api/admin/<string:name>")

if __name__=="__main__":
    with app.app_context():
        app.run(host='0.0.0.0',port=8080)
