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
```
<br />

4. Inicie a aplicação, usando `flask run`
