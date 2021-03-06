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
    
    
class PessoaForm(FlaskForm):
    usuario = StringField('Usuário', validators=[input_required(message="Campo obrigatório")])
    email = StringField('Email', validators=[Email(message="Insira um e-mail válido")])
    senha = PasswordField('Senha', validators=[input_required("Campo obrigatório"), Length(min=8, message="A senha deve conter pelo menos 8 caracteres")])
    confirmar_senha = PasswordField('Confirmação de senha', validators=[input_required('Campo obrigatório'), EqualTo(fieldname='senha', message="As senhas não coincidem")])
    registrar = SubmitField('Registrar')


class EscritorioForm(FlaskForm):


    cnpj = StringField('CNPJ', validators=[input_required(message="Informe apenas os números do CNPJ"), Length(min = 14, max = 14, message = "O CNPJ deve conter 14 caracteres")])
    n_oab = StringField('Nº OAB', validators=[input_required(message="Informe nº OAB no formato UF123456"), Length(min = 8, max = 8, message = "Número inválido, use o formato formato UF123456")])     
    email = StringField('Email', validators=[Email(message="Insira um e-mail válido")])
    senha = PasswordField('Senha', validators=[input_required("Campo obrigatório"), Length(min=8, message="A senha deve conter pelo menos 8 caracteres")])
    confirmar_senha = PasswordField('Confirmação de senha', validators=[input_required('Campo obrigatório'), EqualTo(fieldname='senha', message="As senhas não coincidem")])
    registrar_escritorio = SubmitField('Registrar Escritório')


class CasoForm(FlaskForm):
   nome = StringField('Nome', validators=[input_required(message="Campo obrigatório")])   
   cpf = StringField('CPF', validators=[input_required(message="Informe apenas os números do CPF"), Length(min = 11, max = 11, message = "O CPF deve conter 11 caracteres")])
   descricao = TextAreaField('Descrição do caso',validators=[input_required(message="Campo obrigatório"), Length(max= 1000)])
   enviar = SubmitField('Enviar')
   
   
class PesquisaForm(FlaskForm):
    nome_site = SelectField('Site', choices=[])
    texto_pesquisa = StringField('Pesquisar', validators=[input_required(message="Digite um termo para efetuar a procura")])
    pesquisar = SubmitField('Pesquisar')
    