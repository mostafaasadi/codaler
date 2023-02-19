from app import db
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from sqlalchemy import Column, Integer, String
from wtforms import StringField, PasswordField, SubmitField
from sqlalchemy import Column, Integer, String, Boolean, PickleType
from werkzeug.security import generate_password_hash, check_password_hash

class Audite(db.Model):
    __tablename__ = "audites"
    TrackingNo = Column(Integer, primary_key=True)
    Url = Column(String)
    Title = Column(String)
    Symbol = Column(String)
    PdfUrl = Column(String)
    CompanyName = Column(String)
    SentDateTime = Column(String)
    AttachmentUrl = Column(String)
    PublishDateTime = Column(String)

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(128), nullable=False, unique=False)
    role = Column(Integer(), default=0)
    name = Column(String(32), nullable=True, unique=False)
    authenticated = Column(Boolean, default=False)
    symbols = Column(PickleType, default=[])
    phone = Column(String(10), nullable=True, unique=False)

    def get_id(self):
        return(self.id)

    def is_active(self):
        return(True)

    def is_authenticated(self):
        return self.authenticated

    def check_password(self, password):
        if not password:
            return False
        return check_password_hash(self.password, password)

    def set_password(self, password):
        if not password:
            return False
        self.password = generate_password_hash(password)


class LoginForm(FlaskForm):
    """User Log-in Form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

