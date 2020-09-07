from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField, TextAreaField, SubmitField,
                     PasswordField, DateField, SelectField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length, input_required)


class CadastroForm(FlaskForm):
    usuario = StringField('Usuário', validators=[input_required(message="Campo obrigatório")])
    email = StringField('Email', validators=[Email(message="Insira um e-mail válido")])
    senha = PasswordField('Senha', validators=[input_required("Campo obrigatório"), Length(min=8, message="A senha deve conter pelo menos 8 caracteres")])
    confirmar_senha = PasswordField('Confirmação de senha', validators=[input_required('Campo obrigatório'), EqualTo(fieldname='senha', message="As senhas não coincidem")])
    registrar = SubmitField('Registrar')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email(message="Insira um e-mail válido")])
    senha = PasswordField('Senha', validators=[input_required("Campo obrigatório")])
    entrar = SubmitField('Entrar')