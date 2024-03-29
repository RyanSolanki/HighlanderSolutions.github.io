from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Database object
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fhksdgfkhsdgfsdkfghsdkyhgfdskhfgdskhfghsdkjfhsdkjfhsdjklghfslkjjhbjcvnkhxbvkuih'
    # Database location (.db file in project "website" dir)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .blueprints.views import views
    from .blueprints.auth import auth
    from .blueprints.WorkoutPage import WorkoutPage
    from .blueprints.calender import calender
    from .blueprints.recommender import RecommenderBP

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(WorkoutPage, url_prefix='/')
    app.register_blueprint(calender, url_prefix='/')
    app.register_blueprint(RecommenderBP, url_prefix='/')
    

    from .models import User, Note

    
    create_database(app)
    
    loginManager = LoginManager()
    loginManager.login_view = 'auth.login'
    loginManager.init_app(app)

    @loginManager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        #db.create_all(app=app)
        with app.app_context():
            db.create_all()
        print('Created Database!')
