# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from flask import render_template, flash, redirect, url_for, abort
from flask_login import current_user, login_user, logout_user # для обработки формы логина и разлогина
from sqlalchemy import and_

from app import app, db
from app.forms import LoginForm, RegistrationForm, AreaForm
from app.models import User, Game, SportGround
from config import Config


@app.route('/')
@app.route('/index/')
def index():
    '''
    Главная страница
    :return:
    '''
    return render_template('index.html', title='Home')


@app.route('/login/')
def login():
    '''
    Страница авторизации
    :return:
    '''
    if current_user.is_authenticated:
        flash('Вы уже авторизованы')
        return redirect(url_for('index'))

    form = LoginForm()
    title = "Авторизация"
    return render_template('login.html', title=title, form=form)


@app.route('/process-login/', methods=['POST'])
def process_login():
    '''
    Обработка формы логина
    :return:
    '''
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


@app.route('/register/')
def register():
    '''
    Страница регистрации
    :return:
    '''
    if current_user.is_authenticated:
        flash('Вы уже авторизованы')
        return redirect(url_for('index'))

    form = RegistrationForm()
    title = "Регистрация"
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/process-reg/', methods=['POST'])
def process_reg():
    '''
    Обработка формы регистрации
    :return:
    '''
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


@app.route('/logout/')
def logout():
    '''
    Роут выхода с сайта
    :return:
    '''
    logout_user()
    return redirect(url_for('index'))


@app.route('/sport_ground_choice/')
def sport_ground_choice():
    '''
    Выбор спортивной площадки
    :return:
    '''
    config = Config()
    title = "Выбор спортивной площадки"
    return render_template('sport_ground_choice.html', title=title, key=config)


@app.route('/area/<int:sport_ground_id>/')
def area(sport_ground_id):
    '''
    Страница спорт площадки
    :return:
    '''
    today = datetime.today()
    games = Game.query.filter(Game.sport_ground_id == sport_ground_id).filter(and_(
        Game.start_time >= today,
        Game.start_time < (today + timedelta(days=1)))).order_by(
        Game.start_time).all()

    sport_ground = SportGround.query.filter(SportGround.id == sport_ground_id).first()

    if not sport_ground:
        abort(404)
    form = AreaForm()

    return render_template('sport_ground.html',
                           form=form,
                           title="Спортивная площадка",
                           sport_ground=sport_ground,
                           games=games)


@app.route('/process-area/<int:page_id>/', methods=['POST'])
def process_area(page_id):
    '''
    Обработка формы создания игры
    :return:
    '''
    form = AreaForm()
    if form.validate_on_submit():
        # Оставляем дату и часы, минуты-секунды-микро обнуляем
        start_time = form.game_date.data.replace(minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=int(form.duration_game.data))

        new_game = Game(sport_ground_id=page_id,
                        user_creation_id=current_user.id,
                        start_time=start_time,
                        end_time=end_time,
                        max_players=form.max_players.data,
                        age_range_id=form.age_range.data,
                        game_level_id=form.game_level.data,
                        type_game=form.type_game.data)

        db.session.add(new_game)
        db.session.commit()
        flash('Игра создана!')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
    return redirect(url_for('area', sport_ground_id=page_id))
