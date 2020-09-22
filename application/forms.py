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

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CheckboxForm(FlaskForm):
    string_of_areas = ['Penal\n Tributário\n Civíl\n Trabalhista\n Consumidor\n Empresarial']
    list_of_areas = string_of_areas[0].split()
    # create a list of value/description tuples
    area = [(x, x) for x in list_of_areas]
    areas = MultiCheckboxField('Área', choices=area)

class EscritorioForm(FlaskForm):
    razao_social = StringField('Razão Social', validators=[input_required(message="Campo obrigatório")])
    cnpj = StringField('CNPJ', validators=[input_required(message="Informe apenas os números do CNPJ"), Length(14, message = "CNPJ inválido, informe apenas os números")])
    n_oab = StringField('Nº OAB', validators=[input_required(message="Informe nº OAB no formato UF123456"), Length(8, message = "Número inválido, use o formato formato UF123456")])     
    email = StringField('Email', validators=[Email(message="Insira um e-mail válido")])
    senha = PasswordField('Senha', validators=[input_required("Campo obrigatório"), Length(min=8, message="A senha deve conter pelo menos 8 caracteres")])
    confirmar_senha = PasswordField('Confirmação de senha', validators=[input_required('Campo obrigatório'), EqualTo(fieldname='senha', message="As senhas não coincidem")])
    #area =
    registrar = SubmitField('Registrar')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email(message="Insira um e-mail válido")])
    senha = PasswordField('Senha', validators=[input_required("Campo obrigatório")])
    entrar = SubmitField('Entrar')









