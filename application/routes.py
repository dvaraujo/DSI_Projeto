from flask import request, render_template, redirect, url_for, flash
from flask import current_app as app
from flask_login import login_required, login_user, logout_user, current_user
from .models import Usuario, Escritorio
from .forms import PessoaForm, LoginForm, EscritorioForm
from . import db
from . import login_manager


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

    usuarios = Usuario.query.all()

    return render_template("home.html", usuarios=usuarios)


@app.route("/escritorio")
@login_required
def home_escritorio():

    usuarios = Escritorio.query.all()

    return render_template("escritorio.html", usuarios=usuarios)

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



@app.route("/registro", methods=["POST", "GET"])
def registro():
    form = PessoaForm()
    

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
#@login_required
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




