from flask import request, render_template, redirect, url_for, flash
import requests
from flask import current_app as app
from flask_login import login_required, login_user, logout_user, current_user
from .models import Usuario, Escritorio, Caso
from .forms import CadastroForm, CasoForm, LoginForm, EscritorioForm, PessoaForm
from . import db
from . import login_manager
from oauthlib.oauth2 import WebApplicationClient
import json
import os


GOOGLE_DISCOVERY_URL=os.environ.get("GOOGLE_DISCOVERY_URL")
GOOGLE_CLIENT_ID=os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET=os.environ.get("GOOGLE_CLIENT_SECRET")

client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()



@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return Usuario.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash("Faça login para acessar esta página 😶", category="error")
    return redirect("login")


@app.route("/home")
@login_required
def home():

    usuario = current_user
    casos = usuario.casos
    return render_template("home.html", casos=casos, usuario=usuario)


@app.route("/escritorio")
@login_required
def escritorio():
    escritorio = current_user
    casos = Caso.query.all()

    return render_template("escritorio.html", casos=casos, escritorio=escritorio)


@app.route("/")
@app.route("/login", methods=["POST", "GET"])
def login():

    # Se for POST
    if current_user.is_authenticated:
        return redirect("home")

    form = LoginForm()

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.verifica_senha(senha=form.senha.data):
            login_user(usuario)
            next_page = request.args.get("next")
            return redirect(next_page or "home")
        flash("Combinação de usuário e senha incorreta ☹", category="error")

    # Se for GET
    return render_template("autenticacao/login.html", form=form)


@app.route("/login_escritorio", methods=["POST", "GET"])
def login_escritorio():
    
    # Se for POST
    if current_user.is_authenticated:
        return redirect("escritorio")

    form = LoginForm()

    if form.validate_on_submit():
        usuario = Escritorio.query.filter_by(email=form.email.data).first()
        if usuario and usuario.verifica_senha(senha=form.senha.data):
            login_user(usuario)
            next_page = request.args.get("next")
            return redirect(next_page or "escritorio")
        flash("Combinação de usuário e senha incorreta ☹", category="error")

    # Se for GET
    return render_template("autenticacao/login.html", form=form)


@app.route("/registro_escritorio", methods=["POST", "GET"])
def registro_escritorio():

    form = EscritorioForm()
  

    # Se for POST
    if form.validate_on_submit():       
        cnpj_existe = Escritorio.query.filter_by(cnpj=form.cnpj.data).first()
        oab_existe = Escritorio.query.filter_by(n_oab=form.n_oab.data).first()

        if cnpj_existe is None and oab_existe is None:
            escritorio = Escritorio(
                razao_social=form.razao_social.data,
                cnpj = form.cnpj.data,
                n_oab = form.n_oab.data,               
                email=form.email.data,
            )

            escritorio.set_senha(form.senha.data)
            db.session.add(escritorio)            
            db.session.commit()
            flash("Seu escritório foi cadastrado com sucesso", category="message")
            return redirect("login")
        flash("CNPJ ou Número OAB já cadastrados ☹", category="error")

    # Se for GET
    return render_template("autenticacao/registro_escritorio.html", form=form)


@app.route("/login_google")
def login_google():

    if current_user.is_authenticated:
        return redirect("home")


    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login_google/callback")
def login_google_callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
    token_endpoint,
    authorization_response=request.url,
    redirect_url=request.base_url,
    code=code
    )

    token_response = requests.post(
    token_url,
    headers=headers,
    data=body,
    auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )   

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    print(uri)
    userinfo_response = requests.get(uri, headers=headers, data=body)  
    print(userinfo_response.json()) 

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "Email não disponível ou não autorizado pelo Google!", 400

    # Se o usuário existir    
    usuario = Usuario.query.filter_by(email=users_email).first()
    if usuario:
        login_user(usuario)
        next_page = request.args.get("next")
        return redirect(next_page or url_for("home"))

    # Se o usuário não existir
    usuario = Usuario(
                # Usuário inicialmente será o email da pessoa(antes do dominio), para não conflitar com a constraint unique do banco
                usuario=users_email.split(sep="@")[0],
                email=users_email,
                )
    usuario.set_senha(unique_id)
    db.session.add(usuario)
    db.session.commit()
    login_user(usuario)
    return redirect(url_for("home"))


@app.route("/registro", methods=["POST", "GET"])
def registro():

    form = CadastroForm()

    # Se for POST
    if form.validate_on_submit():
        email_existe = Usuario.query.filter_by(email=form.email.data).first()
        usuario_existe = Usuario.query.filter_by(usuario=form.usuario.data).first()

        if email_existe is None and usuario_existe is None:
            usuario = Usuario(
                usuario=form.usuario.data,
                email=form.email.data,
            )
            usuario.set_senha(form.senha.data)
            db.session.add(usuario)
            db.session.commit()
            flash("Tudo pronto! Agora você já pode fazer o login 😃", category="message")
            return redirect("login")
        flash("Usuário ou email já existe ☹", category="error")

    # Se for GET
    return render_template("autenticacao/registro.html", form=form)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/usuario/<int:usuario_id>", methods=["GET", "POST"])
@login_required
def usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    return render_template("usuario.html", usuario=usuario)


@app.route("/usuario/<int:usuario_id>/editar", methods=["GET", "POST"])
@login_required
def usuario_editar(usuario_id):

    usuario = Usuario.query.get_or_404(usuario_id)

    # Se gor POST
    form = CadastroForm()

    if form.validate_on_submit():
        usuario.usuario = form.usuario.data
        usuario.email = form.email.data
        usuario.set_senha(form.senha.data)
        db.session.commit()
        flash("Usuário alterado", category="message")
        return render_template("usuario.html", usuario=usuario)

    # Se for GET
    return render_template("usuario_editar.html", usuario=usuario, form=form)


@app.route("/usuario/<int:usuario_id>/excluir", methods=["POST"])
@login_required
def usuario_excluir(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuário excluído", category="message")
    return redirect("/home")


@app.route("/caso_adicionar", methods=["POST", "GET"])
def caso_adicionar():

    form = CasoForm()
    usuario_id = current_user.id
    # Se for POST
    if form.validate_on_submit():
        
        caso = Caso(nome=form.nome.data,
                    cpf=form.cpf.data,
                    descricao=form.descricao.data,
                    usuario_id = usuario_id)
        
        db.session.add(caso)
        db.session.commit()
        flash("Caso cadastrado", category="message")
        return redirect("home")
    
    # Se for GET
    return render_template("caso_adicionar.html", form=form)


@app.route("/caso/<int:caso_id>", methods=["GET", "POST"])
@login_required
def caso(caso_id):
    caso = Caso.query.get_or_404(caso_id)
    return render_template("caso.html", caso=caso)


@app.route("/caso/<int:caso_id>/editar", methods=["GET", "POST"])
@login_required
def caso_editar(caso_id):

    caso = Caso.query.get_or_404(caso_id)

    # Se gor POST
    form = CasoForm()

    if form.validate_on_submit():
        caso.nome = form.nome.data
        caso.cpf = form.cpf.data
        caso.descricao = form.descricao.data
        db.session.commit()
        flash("Caso alterado", category="message")
        return render_template("caso.html", caso=caso)

    # Se for GET
    return render_template("caso_editar.html", caso=caso, form=form)


@app.route("/caso/<int:caso_id>/excluir", methods=["POST"])
@login_required
def caso_excluir(caso_id):
    caso = Caso.query.get_or_404(caso_id)
    db.session.delete(caso)
    db.session.commit()
    flash("Caso excluído", category="message")
    return redirect("/home")


@app.route("/escritorio_perfil/<int:escritorio_id>", methods=["GET", "POST"])
@login_required
def escritorio_perfil(escritorio_id):
    escritorio = Escritorio.query.get_or_404(escritorio_id)
    return render_template("escritorio_perfil.html", escritorio=escritorio)


@app.route("/escritorio/<int:escritorio_id>/editar", methods=["GET", "POST"])
@login_required
def escritorio_editar(escritorio_id):

    escritorio = Escritorio.query.get_or_404(escritorio_id)

    # Se gor POST
    form = EscritorioForm()

    if form.validate_on_submit():
        escritorio.razao_social = form.razao_social.data
        escritorio.cnpj = form.cnpj.data
        escritorio.n_oab = form.n_oab.data
        escritorio.email = form.email.data
        escritorio.set_senha(form.senha.data)
        db.session.commit()
        flash("Escritório alterado", category="message")
        return redirect("escritorio_perfil")

    # Se for GET
    return render_template("escritorio_editar.html", escritorio=escritorio, form=form)


@app.route("/escritorio/<int:escritorio_id>/excluir", methods=["POST"])
@login_required
def escritorio_excluir(escritorio_id):
        
    escritorio = Escritorio.query.get_or_404(escritorio_id)
    db.session.delete(escritorio)
    db.session.commit()
    flash("Escritório excluído", category="message")
    return redirect("/login")


