from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField, TextAreaField, SubmitField,
                     PasswordField, DateField, SelectField, SelectMultipleField, widgets)
from wtforms.validators import (DataRequired, Email, EqualTo, Length, input_required)


class PessoaForm(FlaskForm):
    usuario = StringField('Usuário', validators=[input_required(message="Campo obrigatório")])
    email = StringField('Email', validators=[Email(message="Insira um e-mail válido")])
    senha = PasswordField('Senha', validators=[input_required("Campo obrigatório"), Length(min=8, message="A senha deve conter pelo menos 8 caracteres")])
    confirmar_senha = PasswordField('Confirmação de senha', validators=[input_required('Campo obrigatório'), EqualTo(fieldname='senha', message="As senhas não coincidem")])
    registrar = SubmitField('Registrar')


class EscritorioForm(FlaskForm):
    razao_social = StringField('Razão Social', validators=[input_required(message="Campo obrigatório")])
    cnpj = StringField('CNPJ', validators=[input_required(message="Informe apenas os números do CNPJ"), Length(min = 14, max = 14, message = "CNPJ inválido, informe apenas os números")])
    n_oab = StringField('Nº OAB', validators=[input_required(message="Informe nº OAB no formato UF123456"), Length(min = 8, max = 8, message = "Número inválido, use o formato formato UF123456")])     
    email = StringField('Email', validators=[Email(message="Insira um e-mail válido")])
    senha = PasswordField('Senha', validators=[input_required("Campo obrigatório"), Length(min=8, message="A senha deve conter pelo menos 8 caracteres")])
    confirmar_senha = PasswordField('Confirmação de senha', validators=[input_required('Campo obrigatório'), EqualTo(fieldname='senha', message="As senhas não coincidem")])
    registrar_escritorio = SubmitField('Registrar Escritório')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email(message="Insira um e-mail válido")])
    senha = PasswordField('Senha', validators=[input_required("Campo obrigatório")])
    entrar = SubmitField('Entrar')


class CasoForm(FlaskForm):
   nome = StringField('Nome', validators=[input_required(message="Campo obrigatório")])   
   caso = TextAreaField('Descrição do caso',validators=[input_required(message="Campo obrigatório"), Length(max= 1000)])
   enviar = SubmitField('Enviar')