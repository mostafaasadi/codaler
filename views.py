from app import app, db
from requests import get
from fake_headers import Headers
from models import User, LoginForm, Audite
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user


@app.route('/')
@login_required
def index():
    try:
        user = User.query.filter(
                User.username.ilike(current_user.username)).first()
        audites = Audite.query.filter(
            Audite.Symbol.in_(user.symbols)).limit(20)
    except Exception as e:
        print(e)
        audites = []
        flash('خطایی رخ داده است', 'error')
    return render_template(
        'index.html',
        audites=audites
    )


@app.route('/add', methods=['POST', 'GET'])
@login_required
def add_symbol():
    user = User.query.filter(
            User.username.ilike(current_user.username)).first()
    if request.method == 'POST':
        try:
            i_symbols = request.form.getlist('i_symbols[]')
            user.symbols = i_symbols
            db.session.commit()
            flash('نمادها ذخیره شدند', 'success')
        except Exception as e:
            flash('خطایی رخ داده است', 'error')

    try:
        symbols_req = get(
            'https://search.codal.ir/api/search/v1/companies',
            headers=Headers().generate(),
            timeout=3).json()
    except Exception as e:
        return render_template(
            'add.html',
            error=e
        )


    user_symbols = user.symbols
    return render_template(
        'add.html',
        symbols=symbols_req,
        user_symbols=user_symbols
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(
            User.username.ilike(form.username.data)).first()
        if user:
            if user.check_password(form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('login'))
