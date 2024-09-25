from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pedidos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    pagamento = db.Column(db.String(50), nullable=False)
    mensagem = db.Column(db.String(200), nullable=True)

# Criar as tabelas dentro do contexto da aplicação
with app.app_context():
    db.create_all()

# Variável de controle para acesso
PERMITIR_ACESSO = True  # Altere para False para negar acesso

@app.route('/')
def contato():
    return render_template('contato.html', success=False)

@app.route('/enviar-dados', methods=['POST'])
def enviar_dados():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    modelo = request.form.get('modelo')
    pagamento = request.form.get('pagamento')
    mensagem = request.form.get('mensagem')
   
    if nome and email and telefone and modelo and pagamento:
        novo_pedido = Pedido(nome=nome, email=email, telefone=telefone,
                             modelo=modelo, pagamento=pagamento, mensagem=mensagem)
        db.session.add(novo_pedido)
        db.session.commit()
        return render_template('contato.html', success=True)

    return redirect(url_for('contato'))

@app.route('/ver-pedidos')
def ver_pedidos():
    if not PERMITIR_ACESSO:
        flash("Você não tem permissão para acessar esta página.")
        return redirect(url_for('contato'))
   
    pedidos = Pedido.query.all()
    return render_template('ver_pedidos.html', pedidos=pedidos)

if __name__ == '__main__':
    app.run(debug=True)