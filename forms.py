""" Forms """
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    """ Registration / Sign Up form
    """
    first_name = StringField('First Name',
                             validators=[DataRequired()]
                             )

    last_name = StringField('Last Name',
                            validators=[DataRequired()]
                            )

    email = EmailField('Email',
                       validators=[DataRequired()]
                       )

    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=25)]
                             )

    confirm = PasswordField("Repeat password",
                            validators=[
                                DataRequired(),
                                EqualTo("password",
                                        message="Passwords must match."),
                            ],
                            )

# class LoginForm(FlaskForm):
