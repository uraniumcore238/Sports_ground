from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, EqualTo, Email, InputRequired, ValidationError

from app.models import User, AgeRange, GameType, GameLevel


class LoginForm(FlaskForm):
    email = StringField("Почта пользователя",  validators=[InputRequired(message="Почта не введена"),
                                                           Email(message="Почта некорректна")],
                        render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[InputRequired(message="Пароль не введен")],
                             render_kw={"class": "form-control"})
    telegram = StringField('По желанию введите аккаунт telegram, для отправки уведомлений о своих играх',
                           render_kw={"class": "form-control"})
    remember_me = BooleanField('Запомнить меня', default=False, render_kw={"class": "form-check-input"})
    submit = SubmitField('Отправить', render_kw={"class":"btn btn-primary"})


class RegistrationForm(FlaskForm):
    email = StringField("Почта пользователя",
                        validators=[InputRequired(message="Почта не введена"), Email(message="Почта некорректна")],
                        render_kw={"class": "form-control"})
    password = PasswordField('Пароль',
                             validators=[InputRequired(message="Пароль не введен")],
                             render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль',
                              validators=[DataRequired(message="Пароль не введен"),
                                          EqualTo('password', message="Пароли не совпадают")],
                              render_kw={"class": "form-control"})
    telegram = StringField('telegram, для отправки уведомлений о своих играх',
                           render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class":"btn btn-primary"})

    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с таким именем уже зарегистрирован')

class AreaForm(FlaskForm):
    game_date = DateTimeField("ДАТА игры",
                              format='%Y-%m-%dT%H:%M',
                              validators=[InputRequired(message="Дата игры не введена")],
                              render_kw={"class": "form-control",
                                         "type": "datetime-local",
                                         "id": "datetime-local"})
    duration_game = IntegerField("ВРЕМЯ игры в часах",
                                 validators=[InputRequired(message="Время игры не введено")],
                                 render_kw={"class": "form-control"})
    type_game = SelectField("ТИП игры",
                            choices=[(g.id, g.game_type) for g in GameType.query],
                            validate_choice=True,
                            render_kw={"class": "form-select",
                                       "placeholder": "Введите для поиска..."})
    max_players = IntegerField("КОЛИЧЕСТВО игроков",
                                  validators=[InputRequired(message="Количество игроков не введено")],
                                  render_kw={"class": "form-control"})
    age_range = RadioField("ВОЗРАСТ",
                           choices=[(g.id, g.age_range_type) for g in AgeRange.query],
                           validators=[InputRequired(message="Возраст не введен")],
                           render_kw={"class": "form-check-input",
                                        "type": "radio"})
    game_level = RadioField("УРОВЕНЬ игры",
                            choices=[(g.id, g.game_level_type) for g in GameLevel.query],
                            validators=[InputRequired(message="Уровень игры не введен")],
                            render_kw={"class": "form-check-input",
                                       "type": "radio"})

    submit = SubmitField('Отправить', render_kw={"class":"btn btn-sm btn-secondary",
                                                 "type": "submit"})

