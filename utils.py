
def user_add(name, username, password):
    from app import db
    from models import User
    u = User()
    u.name = name
    u.username = username
    u.set_password(password)
    u.role = 1
    db.session.add(u)
    db.session.commit()
