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

# Página HTML simples (poderia ser melhorada com Bootstrap)
TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista de Espera</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <h1 class="mb-4">📋 Lista de Espera</h1>
        <form action="/adicionar" method="POST" class="row g-3 mb-4">
            <div class="col-md-5">
                <input type="text" name="nome" class="form-control" placeholder="Nome" required>
            </div>
            <div class="col-md-5">
                <input type="text" name="telefone" class="form-control" placeholder="Telefone">
            </div>
            <div class="col-md-2 d-grid">
                <button class="btn btn-primary">Adicionar</button>
            </div>
        </form>

        <table class="table table-striped">
            <thead class="table-dark">
                <tr>
                    <th>Nome</th>
                    <th>Telefone</th>
                    <th>Status</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                {% for p in pessoas %}
                <tr>
                    <td>{{ p.nome }}</td>
                    <td>{{ p.telefone or '-' }}</td>
                    <td>{{ p.status }}</td>
                    <td>
                        <a href="/remover/{{ p.id }}" class="btn btn-sm btn-danger">Remover</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

# Cria diretório de templates e grava o arquivo HTML
os.makedirs('templates', exist_ok=True)
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(TEMPLATE_HTML)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
