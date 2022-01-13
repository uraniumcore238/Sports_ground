from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, InputRequired, ValidationError

from app.models import User



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
