## Projeto acadêmico feito na Faculdade Impacta Tecnologia, na matéria de Desenvolvimento de Aplicações Distribuídas

---

<br />

### Como começar

1. Crie e ative um ambiente virtual, por exemplo, usando `python -m venv venv` para criar. Para ativar, use `cd venv\Scripts` e depois `activate` no Windows ou `source venv/bin/activate` no Linux.

<br />

2. Instale as dependências com `pip install -r requirements.txt`.

<br />

3. Crie na raiz do projeto um arquivo de variáveis de ambiente chamado `.env` com as seguintes variáveis:

<br />


```
 FLASK_ENV=development
 SECRET_KEY=CHAVE_SECRETA_AQUI
 SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite3
 GOOGLE_CLIENT_ID=ID_GOOGLE
 GOOGLE_CLIENT_SECRET=SECRET_GOOGLE
 GOOGLE_DISCOVERY_URL=https://accounts.google.com/.well-known/openid-configuration
 STRIPE_SECRET_KEY=SECRET_STRIPE
 STRIPE_PUBLIC_KEY=PUBLIC_STRIPE

```
<br />

3. Faça as migrações usando `flask db upgrade`

4. Inicie a aplicação, usando `flask run`
