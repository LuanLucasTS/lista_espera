from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do banco de dados SQLite
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'waitlist.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de dados
class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(50))
    status = db.Column(db.String(50), default='aguardando')  # aguardando, atendido, cancelado

    def __repr__(self):
        return f'<Pessoa {self.nome}>'

# Cria o banco de dados (caso não exista)
with app.app_context():
    db.create_all()

# Rota principal
@app.route('/')
def index():
    pessoas = Pessoa.query.all()
    return render_template('index.html', pessoas=pessoas)

# Adicionar nova pessoa
@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    if nome:
        nova_pessoa = Pessoa(nome=nome, telefone=telefone)
        db.session.add(nova_pessoa)
        db.session.commit()
    return redirect(url_for('index'))

# Remover pessoa
@app.route('/remover/<int:id>')
def remover(id):
    pessoa = Pessoa.query.get_or_404(id)
    db.session.delete(pessoa)
    db.session.commit()
    return redirect(url_for('index'))

# API: listar pessoas
@app.route('/api/lista', methods=['GET'])
def api_lista():
    pessoas = Pessoa.query.all()
    dados = [{'id': p.id, 'nome': p.nome, 'telefone': p.telefone, 'status': p.status} for p in pessoas]
    return jsonify(dados)

# API: adicionar pessoa
@app.route('/api/adicionar', methods=['POST'])
def api_adicionar():
    data = request.get_json()
    nome = data.get('nome')
    telefone = data.get('telefone')
    if not nome:
        return jsonify({'erro': 'Nome é obrigatório'}), 400
    nova_pessoa = Pessoa(nome=nome, telefone=telefone)
    db.session.add(nova_pessoa)
    db.session.commit()
    return jsonify({'mensagem': 'Pessoa adicionada com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
