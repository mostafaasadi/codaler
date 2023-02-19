
def user_add(name, username, password, phone):
    from app import db
    from models import User
    u = User()
    u.name = name
    u.username = username
    u.set_password(password)
    u.role = 1
    u.symbols = []
    u.phone = phone
    db.session.add(u)
    db.session.commit()

user_add('Mostafa', 'mostafa', '123456', '9998887654')