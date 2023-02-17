from config import Production
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for


app = Flask(__name__)
app.config.from_object(Production)
app.app_context().push()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

from views import *
from models import User
db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return(User.query.get(int(user_id)))


@login_manager.unauthorized_handler
def unauthorized():
    return(redirect(url_for('login')))


if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])
