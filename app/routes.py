# -*- coding: utf-8 -*-
from app import app, db
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user # для обработки формы логина и разлогина
from app.forms import LoginForm, RegistrationForm
from app.models import User


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login')
def login():
    if current_user.is_authenticated:
        flash('Вы уже авторизованы')
        return redirect(url_for('index'))

    form = LoginForm()
    title = "Авторизация"
    return render_template('login.html', title=title, form=form)


@app.route('/process-login', methods=['POST'])
def process_login():

    form = LoginForm()
    user = User.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit() and user.check_password(form.password.data):
        login_user(user, remember=form.remember_me.data)
        flash('Вы вошли на сайт')
        return redirect(url_for('index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
        return redirect(url_for('login'))


@app.route('/register')
def register():
    if current_user.is_authenticated:
        flash('Вы уже авторизованы')
        return redirect(url_for('index'))

    form = RegistrationForm()
    title = "Регистрация"
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(email=form.email.data, telegram=form.telegram.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
        return redirect(url_for('register'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
